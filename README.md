Certainly! Here's a simplified API documentation based on the provided OpenAPI specification:

---

# FastAPI API Documentation

## Register User

**Endpoint:** `/register`

- **Method:** POST
- **Summary:** Register a new user.
- **Request Body:**
  - Content-Type: application/json
  - Schema: UserCreate
    - full_name (string, required): Full Name
    - email (string, required): Email
    - password (string, required): Password
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: UserInResponse
      - fullname (string, required): Fullname
      - email (string, required): Email
  - 422: Validation Error
    - Content-Type: application/json
    - Schema: HTTPValidationError

## Github

**Endpoint:** `/`

- **Method:** GET
- **Summary:** Redirect To Our Github.

## Login For Access Token

**Endpoint:** `/token`

- **Method:** POST
- **Summary:** Login to get an access token.
- **Request Body:**
  - Content-Type: application/x-www-form-urlencoded
  - Schema: Body_login_for_access_token_token_post
    - grant_type (string or null): Grant Type
    - username (string, required): Username
    - password (string, required): Password
    - scope (string, default ""): Scope
    - client_id (string or null): Client Id
    - client_secret (string or null): Client Secret
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
  - 422: Validation Error
    - Content-Type: application/json
    - Schema: HTTPValidationError

## Read Current User

**Endpoint:** `/me`

- **Method:** GET
- **Summary:** Read current user details.
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
    - Schema: UserInResponse
      - fullname (string, required): Fullname
      - email (string, required): Email
  - **Security:** OAuth2PasswordBearer

## Read Nutrition Data

**Endpoint:** `/nutrition`

- **Method:** GET
- **Summary:** Read nutrition data for all items.

## Read Nutrition by Name

**Endpoint:** `/nutrition/{food_name}`

- **Method:** GET
- **Summary:** Read nutrition data for a specific food item.
- **Parameters:**
  - food_name (path, required, string): Food Name
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
  - 422: Validation Error
    - Content-Type: application/json
    - Schema: HTTPValidationError

## Read Chatbot History

**Endpoint:** `/chatbot-history`

- **Method:** GET
- **Summary:** Read chatbot conversation history.
- **Responses:**
  - 200: Successful Response
    - Content-Type: application/json
  - **Security:** OAuth2PasswordBearer
- **Method:** POST
  - **Summary:** Create a new entry in chatbot history.
  - **Request Body:**
    - Content-Type: application/json
    - Schema: ChatbotHistoryCreate
      - message (string, required): Message
      - response (string, required): Response
  - **Responses:**
    - 201: Successful Response
      - Content-Type: application/json
    - 422: Validation Error
      - Content-Type: application/json
      - Schema: HTTPValidationError
    - **Security:** OAuth2PasswordBearer

## Components

### Schemas

- UserCreate:
  - full_name (string, required): Full Name
  - email (string, required): Email
  - password (string, required): Password

- UserInResponse:
  - fullname (string, required): Fullname
  - email (string, required): Email

- HTTPValidationError:
  - detail (array of ValidationError): Detail

- Body_login_for_access_token_token_post:
  - grant_type (string or null): Grant Type
  - username (string, required): Username
  - password (string, required): Password
  - scope (string, default ""): Scope
  - client_id (string or null): Client Id
  - client_secret (string or null): Client Secret

- ChatbotHistoryCreate:
  - message (string, required): Message
  - response (string, required): Response

- ValidationError:
  - loc (array of string or integer, required): Location
  - msg (string, required): Message
  - type (string, required): Error Type

### Security Schemes

- OAuth2PasswordBearer:
  - Type: oauth2
  - Flow: password
  - Token URL: token
  - Scopes: {}

---
