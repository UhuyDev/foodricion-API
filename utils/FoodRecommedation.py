import numpy as np
import pandas as pd
from collections import defaultdict
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import UserMetrics, FoodBookmark, Nutrition, Food

# Define the nutritional parameters for different age groups
NUTRITIONAL_PARAMETERS = {
    (10, 12): {"protein": (34, 46), "serat": (22, 25), "karbohidrat": (130, 260),
               "lemak": (50, 70)},
    (13, 15): {"protein": (46, 52), "serat": (25, 31), "karbohidrat": (130, 260),
               "lemak": (55, 75)},
    (16, 18): {"protein": (52, 56), "serat": (25, 38), "karbohidrat": (130, 260),
               "lemak": (60, 80)},
    (19, 29): {"protein": (46, 56), "serat": (25, 38), "karbohidrat": (130, 260),
               "lemak": (65, 80)},
    (30, 49): {"protein": (46, 56), "serat": (25, 38), "karbohidrat": (130, 260),
               "lemak": (65, 80)},
    (50, 64): {"protein": (46, 56), "serat": (21, 30), "karbohidrat": (130, 260),
               "lemak": (65, 80)},
    (65, 80): {"protein": (46, 56), "serat": (21, 30), "karbohidrat": (130, 260),
               "lemak": (60, 75)},
    (81, float('inf')): {"protein": (46, 56), "serat": (21, 30), "karbohidrat": (130, 260),
                         "lemak": (60, 75)}
}


# Function to get nutritional needs based on age
def get_nutritional_needs(age):
    for age_range, params in NUTRITIONAL_PARAMETERS.items():
        if age_range[0] <= age <= age_range[1]:
            return params
    return None


# Function to calculate nutrition target based on user's current nutrition and needs
def nutrition_target(row, kebutuhan):
    return {
        'protein': kebutuhan['protein'] - row['protein'],
        'karbohidrat': kebutuhan['karbohidrat'] - row['karbohidrat'],
        'serat': kebutuhan['serat'] - row['serat'],
        'lemak': kebutuhan['lemak'] - row['lemak']
    }


# Function to recommend daily food based on user's nutritional needs and consumption history
def recommend_daily_food(user_id: str, db: Session):
    # Get user metrics
    user_metrics = db.query(UserMetrics).filter(UserMetrics.user_id == user_id).first()
    if not user_metrics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User metrics not found")

    age = user_metrics.age

    nutritional_needs = get_nutritional_needs(age)
    if not nutritional_needs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Age range not supported")

    # Get today's date in UTC
    today = datetime.now(timezone.utc).date()

    # Get food bookmarks for the current day
    bookmarks = db.query(FoodBookmark).filter(FoodBookmark.user_id == user_id,
                                              func.date(FoodBookmark.bookmark_date) == today).all()

    # Count occurrences of each food item in bookmarks
    food_count = defaultdict(int)
    for bookmark in bookmarks:
        food_count[bookmark.food_id] += 1

    # Calculate total nutritional values consumed
    total_nutrition = {key: 0 for key in nutritional_needs.keys()}
    for food_id, count in food_count.items():
        nutrition = db.query(Nutrition).filter(Nutrition.food_id == food_id).first()
        if nutrition:
            total_nutrition["protein"] += (nutrition.protein or 0) * count
            total_nutrition["serat"] += (nutrition.dietary_fiber or 0) * count
            total_nutrition["karbohidrat"] += (nutrition.total_carbohydrate or 0) * count
            total_nutrition["lemak"] += (nutrition.total_fat or 0) * count

    # Calculate remaining nutritional needs
    remaining_nutrition = {key: max(nutritional_needs[key][1] - total_nutrition[key], 0) for key in
                           nutritional_needs.keys()}

    # Calculate the ratio of total nutrition consumed to minimum nutrition needs
    ratio_nutrition = {key: total_nutrition[key] / nutritional_needs[key][1] if nutritional_needs[key][1] > 0 else 0
                       for key in nutritional_needs.keys()}

    # Determine which nutrient is most deficient based on the minimum ratio
    most_deficient_nutrient = min(ratio_nutrition, key=ratio_nutrition.get)

    # Check if all remaining nutritional needs are zero
    if all(value == 0 for value in remaining_nutrition.values()):
        return {
            "status": "success",
            "message": "Nutritional requirements already met for today",
            "data": None
        }

    # Get all food items
    food_all = db.query(Food, Nutrition).join(Nutrition, Food.food_id == Nutrition.food_id).all()

    data_list = []
    for food, nutrition in food_all:
        data_list.append({
            'food_name': food.food_name,
            "protein": nutrition.protein,
            "serat": nutrition.dietary_fiber,
            "karbohidrat": nutrition.total_carbohydrate,
            "lemak": nutrition.total_fat
        })

    food_df = pd.DataFrame(data_list)
    food_df.fillna(0, inplace=True)

    scaler = StandardScaler()
    nutrition = food_df[['protein', 'karbohidrat', 'serat', 'lemak']]
    nutrition_scaled = scaler.fit_transform(nutrition)

    food_data_scaled = pd.concat(
        [food_df[['food_name']], pd.DataFrame(nutrition_scaled, columns=['protein', 'karbohidrat', 'serat', 'lemak'])],
        axis=1)
    food_data_scaled['target'] = food_data_scaled.apply(lambda row: nutrition_target(row, total_nutrition), axis=1)

    x = food_data_scaled[['protein', 'karbohidrat', 'serat', 'lemak']]
    model = NearestNeighbors(n_neighbors=5, algorithm='auto')
    model.fit(x)

    target_nutrition = np.array([
        remaining_nutrition.get("protein"),
        remaining_nutrition.get("serat"),
        remaining_nutrition.get("karbohidrat"),
        remaining_nutrition.get("lemak")
    ])
    distance, index = model.kneighbors([target_nutrition])
    recommended_foods = food_df.iloc[index[0]].to_dict(orient='records')

    return {
        "status": "success",
        "message": "Recommended food items retrieved successfully",
        "data": recommended_foods
    }
