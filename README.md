## FastAPI API Documentation

### Welcome
- **GET** `/`
  - **Summary:** Welcome
  - **Operation ID:** welcome__get
  - **Description:** Endpoint to welcome users.
  - **Responses:**
    - 200: Successful Response
      - Content: application/json
        - Schema: Empty

### Register User
- **POST** `/register`
  - **Summary:** Register User
  - **Operation ID:** register_user_register_post
  - **Description:** Endpoint to register a new user.
  - **Request Body:**
    - Content: application/json
      - Schema: UserCreate
  - **Responses:**
    - 200: Successful Response
      - Content: application/json
        - Schema: UserInResponse
    - 422: Validation Error
      - Content: application/json
        - Schema: HTTPValidationError

### Login For Access Token
- **POST** `/token`
  - **Summary:** Login For Access Token
  - **Operation ID:** login_for_access_token_token_post
  - **Description:** Endpoint for user login and access token generation.
  - **Request Body:**
    - Content: application/x-www-form-urlencoded
      - Schema: Body_login_for_access_token_token_post
  - **Responses:**
    - 200: Successful Response
      - Content: application/json
        - Schema: Empty
    - 422: Validation Error
      - Content: application/json
        - Schema: HTTPValidationError

### Read Current User
- **GET** `/me`
  - **Summary:** Read Current User
  - **Operation ID:** read_current_user_me_get
  - **Description:** Endpoint to retrieve current user details.
  - **Responses:**
    - 200: Successful Response
      - Content: application/json
        - Schema: UserInResponse
  - **Security:**
    - OAuth2PasswordBearer

### Read Nutrition All
- **GET** `/nutrition`
  - **Summary:** Read Nutrition All
  - **Operation ID:** read_nutrition_all_nutrition_get
  - **Description:** Endpoint to retrieve all nutrition data.
  - **Responses:**
    - 200: Successful Response
      - Content: application/json
        - Schema: Empty

### Read Nutrition Name
- **GET** `/nutrition/{food_name}`
  - **Summary:** Read Nutrition Name
  - **Operation ID:** read_nutrition_name_nutrition__food_name__get
  - **Description:** Endpoint to retrieve nutrition data by food name.
  - **Parameters:**
    - food_name (path, string): Food Name
  - **Responses:**
    - 200: Successful Response
      - Content: application/json
        - Schema: Empty
    - 422: Validation Error
      - Content: application/json
        - Schema: HTTPValidationError

### Read Chatbot History
- **GET** `/chatbot-history`
  - **Summary:** Read Chatbot History
  - **Operation ID:** read_chatbot_history_chatbot_history_get
  - **Description:** Endpoint to retrieve chatbot conversation history.
  - **Responses:**
    - 200: Successful Response
      - Content: application/json
        - Schema: Empty
  - **Security:**
    - OAuth2PasswordBearer

### Create Chatbot History
- **POST** `/chatbot-history`
  - **Summary:** Create Chatbot History
  - **Operation ID:** create_chatbot_history_chatbot_history_post
  - **Description:** Endpoint to create chatbot conversation history.
  - **Request Body:**
    - Content: application/json
      - Schema: ChatbotHistoryCreate
  - **Responses:**
    - 201: Successful Response
      - Content: application/json
        - Schema: Empty
    - 422: Validation Error
      - Content: application/json
        - Schema: HTTPValidationError
  - **Security:**
    - OAuth2PasswordBearer

---

This documentation outlines the available endpoints, their methods, summaries, operation IDs, descriptions, request/response details, and security requirements.
