from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from collections import defaultdict

from models import UserMetrics, FoodBookmark, Nutrition, Food

# Define the nutritional parameters for different age groups
NUTRITIONAL_PARAMETERS = {
    (10, 12): {"Kalori": (1600, 2200), "Protein": (34, 46), "Serat": (22, 25), "Karbohidrat": (130, 260),
               "Lemak": (50, 70)},
    (13, 15): {"Kalori": (1800, 2400), "Protein": (46, 52), "Serat": (25, 31), "Karbohidrat": (130, 260),
               "Lemak": (55, 75)},
    (16, 18): {"Kalori": (2000, 2600), "Protein": (52, 56), "Serat": (25, 38), "Karbohidrat": (130, 260),
               "Lemak": (60, 80)},
    (19, 29): {"Kalori": (2000, 2600), "Protein": (46, 56), "Serat": (25, 38), "Karbohidrat": (130, 260),
               "Lemak": (65, 80)},
    (30, 49): {"Kalori": (1800, 2400), "Protein": (46, 56), "Serat": (25, 38), "Karbohidrat": (130, 260),
               "Lemak": (65, 80)},
    (50, 64): {"Kalori": (1600, 2200), "Protein": (46, 56), "Serat": (21, 30), "Karbohidrat": (130, 260),
               "Lemak": (65, 80)},
    (65, 80): {"Kalori": (1600, 2200), "Protein": (46, 56), "Serat": (21, 30), "Karbohidrat": (130, 260),
               "Lemak": (60, 75)},
    (81, float('inf')): {"Kalori": (1400, 2000), "Protein": (46, 56), "Serat": (21, 30), "Karbohidrat": (130, 260),
                         "Lemak": (60, 75)}
}


def get_nutritional_needs(age):
    for age_range, params in NUTRITIONAL_PARAMETERS.items():
        if age_range[0] <= age <= age_range[1]:
            return params
    return None


def recommend_daily_food(user_id: str, db: Session):
    # Get user metrics
    user_metrics = db.query(UserMetrics).filter(UserMetrics.user_id == user_id).first()
    if not user_metrics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User metrics not found")

    age = user_metrics.age
    print(f"User age: {age}")

    nutritional_needs = get_nutritional_needs(age)
    if not nutritional_needs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Age range not supported")

    print(f"Nutritional needs: {nutritional_needs}")

    # Get today's date in UTC
    today = datetime.now(timezone.utc).date()
    print(f"Today's date: {today}")

    # Get food bookmarks for the current day
    bookmarks = db.query(FoodBookmark).filter(FoodBookmark.user_id == user_id,
                                              func.date(FoodBookmark.bookmark_date) == today).all()
    print(f"Number of bookmarks for today: {len(bookmarks)}")

    # Count occurrences of each food item in bookmarks
    food_count = defaultdict(int)
    for bookmark in bookmarks:
        food_count[bookmark.food_id] += 1

    print(f"Food count: {food_count}")

    # Calculate total nutritional values consumed
    total_nutrition = {key: 0 for key in nutritional_needs.keys()}
    for food_id, count in food_count.items():
        nutrition = db.query(Nutrition).filter(Nutrition.food_id == food_id).first()
        if nutrition:
            total_nutrition["Kalori"] += (nutrition.energy or 0) * count
            total_nutrition["Protein"] += (nutrition.protein or 0) * count
            total_nutrition["Serat"] += (nutrition.dietary_fiber or 0) * count
            total_nutrition["Karbohidrat"] += (nutrition.total_carbohydrate or 0) * count
            total_nutrition["Lemak"] += (nutrition.total_fat or 0) * count

    print(f"Total nutrition consumed: {total_nutrition}")

    # Calculate remaining nutritional needs
    remaining_nutrition = {key: max(nutritional_needs[key][1] - total_nutrition[key], 0) for key in
                           nutritional_needs.keys()}
    print(f"Remaining nutritional needs: {remaining_nutrition}")

    # Check if all remaining nutritional needs are zero
    if all(value == 0 for value in remaining_nutrition.values()):
        return {
            "status": "success",
            "message": "Nutritional requirements already met for today",
            "data": None
        }

    # Get all food items
    food_all = db.query(Food, Nutrition).join(Nutrition, Food.food_id == Nutrition.food_id).all()
    print(f"Number of food items: {len(food_all)}")

    # Create a DataFrame for food items and their nutritional values
    food_df = pd.DataFrame([{
        "food_id": food.food_id,
        "food_name": food.food_name,
        "Kalori": nutrition.energy or 0,
        "Protein": nutrition.protein or 0,
        "Serat": nutrition.dietary_fiber or 0,
        "Karbohidrat": nutrition.total_carbohydrate or 0,
        "Lemak": nutrition.total_fat or 0
    } for food, nutrition in food_all])

    print(f"Food DataFrame shape: {food_df.shape}")

    # Create a DataFrame for remaining nutritional needs
    needs_df = pd.DataFrame([remaining_nutrition])
    print(f"Needs DataFrame shape: {needs_df.shape}")

    # Calculate cosine similarity between food items and remaining nutritional needs
    similarity_scores = cosine_similarity(food_df[["Kalori", "Protein", "Serat", "Karbohidrat", "Lemak"]], needs_df)
    print(f"Similarity scores shape: {similarity_scores.shape}")

    # Get the most similar food items
    similar_food_indices = similarity_scores.argsort(axis=0)[-5:][::-1].flatten()
    print(f"Most similar food indices: {similar_food_indices}")

    recommended_foods = food_df.iloc[similar_food_indices]
    print(f"Recommended foods: {recommended_foods}")

    return {
        "status": "success",
        "message": "Recommended food items retrieved successfully",
        "data": recommended_foods[["food_name", "Kalori", "Protein", "Serat", "Karbohidrat", "Lemak"]].to_dict(
            orient="records")
    }
