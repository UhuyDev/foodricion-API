# FastAPI OpenAPI Specification

## Endpoints

### Register User

- **Method:** POST
- **Summary:** Register User
- **Operation ID:** register_user_register_post
- **Request Body:**
  - Content-Type: application/json
  - Schema: [UserCreate](#usercreate)
  - Required: Yes
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: [UserInResponse](#userinresponse)
  - 422: Validation Error
    - Content-Type: application/json
    - Schema: [HTTPValidationError](#httpvalidationerror)

### Github

- **Method:** GET
- **Summary:** Github
- **Operation ID:** github__get
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: (empty)

### Login For Access Token

- **Method:** POST
- **Summary:** Login For Access Token
- **Operation ID:** login_for_access_token_token_post
- **Request Body:**
  - Content-Type: application/x-www-form-urlencoded
  - Schema: [Body_login_for_access_token_token_post](#body_login_for_access_token_token_post)
  - Required: Yes
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: (empty)
  - 422: Validation Error
    - Content-Type: application/json
    - Schema: [HTTPValidationError](#httpvalidationerror)

### Read Current User

- **Method:** GET
- **Summary:** Read Current User
- **Operation ID:** read_current_user_me_get
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: [UserInResponse](#userinresponse)
- **Security:**
  - OAuth2PasswordBearer

### Read Nutrition All

- **Method:** GET
- **Summary:** Read Nutrition All
- **Operation ID:** read_nutrition_all_nutrition_get
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: (empty)

### Read Nutrition Name

- **Method:** GET
- **Summary:** Read Nutrition Name
- **Operation ID:** read_nutrition_name_nutrition__food_name__get
- **Parameters:**
  - food_name (path, required, string): Food Name
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: (empty)
  - 422: Validation Error
    - Content-Type: application/json
    - Schema: [HTTPValidationError](#httpvalidationerror)

### Read Chatbot History

- **Method:** GET
- **Summary:** Read Chatbot History
- **Operation ID:** read_chatbot_history_chatbot_history_get
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: (empty)
- **Security:**
  - OAuth2PasswordBearer

### Create Chatbot History

- **Method:** POST
- **Summary:** Create Chatbot History
- **Operation ID:** create_chatbot_history_chatbot_history_post
- **Request Body:**
  - Content-Type: application/json
  - Schema: [ChatbotHistoryCreate](#chatbothistorycreate)
  - Required: Yes
- **Responses:**
  - 201: Successful Response
    - Content-Type: application/json
    - Schema: (empty)
  - 422: Validation Error
    - Content-Type: application/json
    - Schema: [HTTPValidationError](#httpvalidationerror)
- **Security:**
  - OAuth2PasswordBearer

## Components

### Schemas

- **UserCreate:** [UserCreate](#usercreate)
  - full_name (string, required): Full Name
  - email (string, required): Email
  - password (string, required): Password

- **UserInResponse:** [UserInResponse](#userinresponse)
  - fullname (string, required): Fullname
  - email (string, required): Email

- **HTTPValidationError:** [HTTPValidationError](#httpvalidationerror)
  - detail (array of ValidationError): Detail

- **Body_login_for_access_token_token_post:** [Body_login_for_access_token_token_post](#body_login_for_access_token_token_post)
  - grant_type (string or null): Grant Type
  - username (string, required): Username
  - password (string, required): Password
  - scope (string, default ""): Scope
  - client_id (string or null): Client Id
  - client_secret (string or null): Client Secret

- **ChatbotHistoryCreate:** [ChatbotHistoryCreate](#chatbothistorycreate)
  - message (string, required): Message
  - response (string, required): Response

- **ValidationError:** [ValidationError](#validationerror)
  - loc (array of string or integer, required): Location
  - msg (string, required): Message
  - type (string, required): Error Type

### Security Schemes

- **OAuth2PasswordBearer:**
  - Type: oauth2
  - Flow: password
  - Token URL: token
  - Scopes: {}
