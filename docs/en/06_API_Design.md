# SentinelAI Phase 1 API Design

## 1. Document Information

| Item             | Value                        |
| ---------------- | ---------------------------- |
| Project          | SentinelAI                   |
| Document         | Phase 1 API Design           |
| Phase            | Phase 1 - Authentication MVP |
| Status           | Draft                        |
| API Style        | REST-style JSON API          |
| Backend          | FastAPI                      |
| Primary Language | English                      |
| Last Updated     | 2026-07-11                   |

## 2. Purpose

This document defines the API contract for the SentinelAI Phase 1 Authentication MVP.

The API supports:

* Health checking
* User registration
* User login
* Authenticated-user retrieval
* Logout

This document defines endpoint paths, request bodies, response bodies, authentication requirements, status codes, validation behavior, and error responses.

## 3. API Scope

### 3.1 In Scope

* JSON request and response bodies
* API versioning
* Registration endpoint
* Login endpoint
* Current-user endpoint
* Logout endpoint
* Health-check endpoint
* HttpOnly cookie authentication
* Request validation
* Consistent error responses

### 3.2 Out of Scope

The following are not part of Phase 1:

* Refresh-token endpoints
* Password reset
* Email verification
* Role and permission APIs
* Organization APIs
* Log APIs
* AI APIs
* Alert APIs
* Monitoring APIs
* API-key authentication
* OAuth or external identity providers

## 4. Base URL

Development base URL:

```text
http://localhost:8000
```

API prefix:

```text
/api/v1
```

Example endpoint:

```text
http://localhost:8000/api/v1/auth/login
```

All Phase 1 business endpoints must use the `/api/v1` prefix.

## 5. Content Type

Requests with JSON bodies must use:

```http
Content-Type: application/json
```

Successful API responses should use:

```http
Content-Type: application/json
```

## 6. Authentication Mechanism

SentinelAI Phase 1 uses a JWT access token transported in an HttpOnly cookie.

Cookie name:

```text
sentinelai_access_token
```

The frontend must send credentialed requests.

Example using the browser Fetch API:

```typescript
fetch("http://localhost:8000/api/v1/auth/me", {
  method: "GET",
  credentials: "include"
});
```

Example using Axios:

```typescript
axios.get("http://localhost:8000/api/v1/auth/me", {
  withCredentials: true
});
```

The JWT must not be returned to frontend JavaScript in the response body.

## 7. Common Response Conventions

### 7.1 Success Responses

Successful responses should return only the data required by the client.

Example:

```json
{
  "id": "2e12955d-4df8-4bde-9207-459e5fbbd263",
  "username": "sai",
  "email": "sai@example.com",
  "is_active": true,
  "created_at": "2026-07-11T10:00:00Z"
}
```

### 7.2 Error Responses

FastAPI-compatible error responses use:

```json
{
  "detail": "Error message"
}
```

Example:

```json
{
  "detail": "Invalid email or password"
}
```

### 7.3 Validation Errors

Request-schema validation errors may use FastAPI's structured validation response:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 12 characters",
      "input": "example"
    }
  ]
}
```

The exact validation format should remain consistent across endpoints.

## 8. Common Status Codes

| Status                      | Meaning                                     | Usage                                         |
| --------------------------- | ------------------------------------------- | --------------------------------------------- |
| `200 OK`                    | Request completed successfully              | Login, logout, current user, health check     |
| `201 Created`               | Resource created successfully               | User registration                             |
| `400 Bad Request`           | Business validation failed                  | Password policy or malformed business input   |
| `401 Unauthorized`          | Authentication failed or is missing         | Invalid login, missing or invalid JWT         |
| `403 Forbidden`             | Authenticated account is not allowed access | Inactive user                                 |
| `409 Conflict`              | Resource conflicts with existing data       | Duplicate email or username                   |
| `422 Unprocessable Entity`  | Request-schema validation failed            | Invalid request body                          |
| `500 Internal Server Error` | Unexpected server failure                   | Unhandled backend error                       |
| `503 Service Unavailable`   | Dependency unavailable                      | Optional readiness or database health failure |

## 9. Public User Response Object

The public user response object contains:

| Field        | Type              | Required | Description                |
| ------------ | ----------------- | -------: | -------------------------- |
| `id`         | UUID string       |      Yes | Stable user identifier     |
| `username`   | String            |      Yes | Normalized username        |
| `email`      | Email string      |      Yes | Normalized email address   |
| `is_active`  | Boolean           |      Yes | Account-access status      |
| `created_at` | ISO 8601 datetime |      Yes | Account creation timestamp |

Example:

```json
{
  "id": "2e12955d-4df8-4bde-9207-459e5fbbd263",
  "username": "sai",
  "email": "sai@example.com",
  "is_active": true,
  "created_at": "2026-07-11T10:00:00Z"
}
```

The response must never contain:

* `password`
* `password_hash`
* JWT values
* JWT signing secrets
* Database credentials

## 10. Endpoint Summary

| ID      | Method | Path                    | Authentication  | Purpose                            |
| ------- | ------ | ----------------------- | --------------- | ---------------------------------- |
| API-001 | GET    | `/health`               | Public          | Basic application health check     |
| API-001A | GET   | `/health/ready`         | Public          | Check database readiness           |
| API-002 | POST   | `/api/v1/auth/register` | Public          | Register a new user                |
| API-003 | POST   | `/api/v1/auth/login`    | Public          | Authenticate a user and set cookie |
| API-004 | GET    | `/api/v1/auth/me`       | Required        | Return the authenticated user      |
| API-005 | POST   | `/api/v1/auth/logout`   | Cookie optional | Clear authentication cookie        |

## 11. API-001: Health Check

### 11.1 Endpoint

```http
GET /health
```

### 11.2 Authentication

Not required.

### 11.3 Purpose

Confirms that the FastAPI application process is running and able to respond.

### 11.4 Successful Response

```http
200 OK
```

```json
{
  "status": "ok",
  "service": "sentinelai-backend"
}
```

### 11.5 Notes

The Phase 1 health endpoint does not need to expose:

* Database credentials
* Environment values
* Version-control information
* Host details
* Secret configuration

A separate readiness check verifies database connectivity without changing the purpose of the basic health endpoint.

## Database Readiness Check

### Endpoint

```http
GET /health/ready
```

### Purpose

Confirms that the backend can execute a basic PostgreSQL query.

### Successful Response

```http
200 OK
```

```json
{
  "status": "ready",
  "database": "available"
}
```

### Unavailable Database

```http
503 Service Unavailable
```

```json
{
  "detail": "Database is unavailable"
}
```

The response must not expose database connection details.

---

## 12. API-002: User Registration

### 12.1 Endpoint

```http
POST /api/v1/auth/register
```

### 12.2 Authentication

Not required.

### 12.3 Request Body

| Field      | Type         | Required | Rules                                       |
| ---------- | ------------ | -------: | ------------------------------------------- |
| `username` | String       |      Yes | 3-50 characters; letters, numbers, `_`, `-` |
| `email`    | Email string |      Yes | Valid email; normalized to lowercase        |
| `password` | String       |      Yes | 12-128 characters; password policy applies  |

Example:

```json
{
  "username": "sai",
  "email": "sai@example.com",
  "password": "ExamplePassword123!"
}
```

The password-confirmation field belongs to the frontend form and is not required by the API because the backend receives only the final password value.

### 12.4 Processing Rules

The backend must:

1. Validate the request schema.
2. Trim and normalize the username.
3. Trim and lowercase the email.
4. Validate the password policy.
5. Check for duplicate username or email.
6. Hash the password using Argon2.
7. Create the user in a transaction.
8. Return the public user response.

### 12.5 Successful Response

```http
201 Created
```

```json
{
  "id": "2e12955d-4df8-4bde-9207-459e5fbbd263",
  "username": "sai",
  "email": "sai@example.com",
  "is_active": true,
  "created_at": "2026-07-11T10:00:00Z"
}
```

Registration does not automatically log the user in during Phase 1.

After registration, the frontend should redirect the user to the login page.

### 12.6 Error Responses

#### Invalid Password Policy

```http
400 Bad Request
```

```json
{
  "detail": "Password does not meet the required security policy"
}
```

#### Duplicate Email

```http
409 Conflict
```

```json
{
  "detail": "An account with this email already exists"
}
```

#### Duplicate Username

```http
409 Conflict
```

```json
{
  "detail": "This username is already in use"
}
```

#### Request Validation Failure

```http
422 Unprocessable Entity
```

FastAPI validation-response structure.

### 12.7 Security Requirements

* Do not return the password or password hash.
* Do not log the plaintext password.
* Do not expose database exceptions directly.
* Database unique constraints remain the final protection against duplicates.

### Implementation Status

`POST /api/v1/auth/register` is implemented with:

* Request validation
* Username and email normalization
* Argon2 password hashing
* Duplicate email detection
* Duplicate username detection
* PostgreSQL persistence
* Safe public response schema

## 13. API-003: User Login

### 13.1 Endpoint

```http
POST /api/v1/auth/login
```

### 13.2 Authentication

Not required.

### 13.3 Request Body

| Field      | Type         | Required | Rules                                             |
| ---------- | ------------ | -------: | ------------------------------------------------- |
| `email`    | Email string |      Yes | Trimmed and normalized to lowercase               |
| `password` | String       |      Yes | Plaintext input used only for secure verification |

Example:

```json
{
  "email": "sai@example.com",
  "password": "ExamplePassword123!"
}
```

### 13.4 Processing Rules

The backend must:

1. Validate the request body.
2. Normalize the email to lowercase.
3. Find the user by email.
4. Reject inactive users with `403 Forbidden`.
5. Verify the password using the stored Argon2 hash.
6. Create a JWT access token with a 30-minute lifetime.
7. Set the JWT in the HttpOnly cookie.
8. Return a safe success response.

### 13.5 Successful Response

```http
200 OK
```

Response header conceptually contains:

```http
Set-Cookie: sentinelai_access_token=<jwt>; HttpOnly; SameSite=Lax; Path=/; Max-Age=1800
```

Development environments use:

```text
Secure=false
```

Production environments use:

```text
Secure=true
```

Response body:

```json
{
  "message": "Login successful"
}
```

### 13.6 Error Responses

#### Invalid Credentials

```http
401 Unauthorized
```

```json
{
  "detail": "Invalid email or password"
}
```

Use the same message when:

* The email does not exist
* The password is incorrect

#### Inactive User

```http
403 Forbidden
```

```json
{
  "detail": "Account access is disabled"
}
```

#### Request Validation Failure

```http
422 Unprocessable Entity
```

### 13.7 Security Requirements

* Do not return the JWT in JSON.
* Do not expose whether an email exists through credential errors.
* Do not log the submitted password.
* Do not log the JWT.
* Cookie attributes must match the approved environment configuration.

## 14. API-004: Current Authenticated User

### 14.1 Endpoint

```http
GET /api/v1/auth/me
```

### 14.2 Authentication

Required.

The browser must send:

```text
sentinelai_access_token
```

as an HttpOnly cookie.

### 14.3 Request Body

None.

### 14.4 Processing Rules

The backend must:

1. Read the authentication cookie.
2. Reject the request if the cookie is missing.
3. Decode the JWT.
4. Verify the JWT signature.
5. Verify expiration.
6. Verify token type.
7. Read the user UUID from `sub`.
8. Load the user from PostgreSQL.
9. Verify the account is active.
10. Return the public user response.

### 14.5 Successful Response

```http
200 OK
```

```json
{
  "id": "2e12955d-4df8-4bde-9207-459e5fbbd263",
  "username": "sai",
  "email": "sai@example.com",
  "is_active": true,
  "created_at": "2026-07-11T10:00:00Z"
}
```

### 14.6 Error Responses

#### Missing Cookie

```http
401 Unauthorized
```

```json
{
  "detail": "Authentication required"
}
```

#### Invalid or Expired JWT

```http
401 Unauthorized
```

```json
{
  "detail": "Invalid or expired authentication session"
}
```

#### User Not Found

```http
401 Unauthorized
```

```json
{
  "detail": "Invalid authentication session"
}
```

#### Inactive User

```http
403 Forbidden
```

```json
{
  "detail": "Account access is disabled"
}
```

### 14.7 Security Requirements

* Do not expose the password hash.
* Do not distinguish unnecessary token-validation details to the client.
* Backend authentication must run on every protected request.
* Frontend route state is not sufficient authorization.

## 15. API-005: Logout

### 15.1 Endpoint

```http
POST /api/v1/auth/logout
```

### 15.2 Authentication

A valid authentication cookie is not strictly required.

The endpoint should remain safe and idempotent when:

* A valid cookie exists
* An expired cookie exists
* No cookie exists

### 15.3 Request Body

None.

### 15.4 Processing Rules

The backend must clear the authentication cookie using the same:

* Cookie name
* Path
* Domain, when configured
* Security context

The response should set:

```text
Empty cookie value
Max-Age = 0
Expired timestamp
```

### 15.5 Successful Response

```http
200 OK
```

```json
{
  "message": "Logout successful"
}
```

### 15.6 Error Behavior

Logout should normally return success even when no active cookie exists.

This makes logout idempotent and simplifies frontend session cleanup.

### 15.7 Security Requirements

* Do not return the previous JWT.
* Do not log the cookie value.
* Ensure deletion attributes match the original cookie configuration.

## 16. CORS Requirements

Because the frontend and backend may use different localhost ports during development, CORS must be configured explicitly.

Example frontend origin:

```text
http://localhost:5173
```

Backend CORS rules must:

* Allow only configured frontend origins
* Allow credentials
* Allow required methods
* Allow required headers
* Never combine credentialed requests with wildcard origins

Conceptual FastAPI behavior:

```text
allow_origins = configured frontend origins
allow_credentials = true
allow_methods = required methods
allow_headers = required headers
```

Production origins must be configured separately.

## 17. Cookie Requirements

Development settings:

| Attribute | Value                     |
| --------- | ------------------------- |
| Name      | `sentinelai_access_token` |
| HttpOnly  | `true`                    |
| Secure    | `false`                   |
| SameSite  | `Lax`                     |
| Path      | `/`                       |
| Max-Age   | `1800` seconds            |

Production settings:

| Attribute | Value                     |
| --------- | ------------------------- |
| Name      | `sentinelai_access_token` |
| HttpOnly  | `true`                    |
| Secure    | `true`                    |
| SameSite  | `Lax` or stricter         |
| Path      | `/`                       |
| Max-Age   | `1800` seconds            |
| HTTPS     | Required                  |

## 18. Input Validation Rules

### 18.1 Username

```text
Minimum length: 3
Maximum length: 50
Pattern: ^[A-Za-z0-9_-]{3,50}$
```

### 18.2 Email

```text
Maximum length: 254
Trim whitespace
Normalize to lowercase
Validate email format
```

### 18.3 Password

```text
Minimum length: 12
Maximum length: 128
At least one uppercase character
At least one lowercase character
At least one number
At least one special character
```

The backend remains authoritative for all validation.

## 19. API Security Rules

* Use HTTPS in production.
* Use HttpOnly authentication cookies.
* Use Secure cookies in production.
* Restrict CORS origins.
* Never return password hashes.
* Never return JWT signing secrets.
* Never log passwords or JWTs.
* Validate all request bodies.
* Use consistent authentication errors.
* Handle database exceptions safely.
* Avoid exposing stack traces in production.
* Enforce authentication in backend dependencies.
* Consider CSRF protection before production deployment.

## 20. Logging Rules

The API may log:

* Endpoint path
* HTTP method
* Status code
* Request duration
* Request correlation identifier
* Authentication success without token content
* Authentication failure without credentials
* Unexpected application errors

The API must not log:

* Passwords
* Password hashes
* JWT values
* Cookie values
* Database passwords
* Signing secrets

## 21. Test Requirements

### Health Check

* Returns `200`
* Returns expected service status
* Readiness check returns `200` when PostgreSQL is available
* Readiness check returns `503` when PostgreSQL is unavailable
* Readiness errors do not expose database connection details

### Registration

* Valid registration returns `201`
* Invalid body returns `422`
* Weak password returns `400`
* Duplicate email returns `409`
* Duplicate username returns `409`
* Password hash is never returned

### Login

* Valid credentials return `200`
* Authentication cookie is created
* Cookie is HttpOnly
* Invalid credentials return `401`
* Inactive user returns `403`
* JWT is not returned in JSON

### Current User

* Valid cookie returns `200`
* Missing cookie returns `401`
* Invalid JWT returns `401`
* Expired JWT returns `401`
* Unknown user returns `401`
* Inactive user returns `403`

### Logout

* Valid cookie is cleared
* Missing cookie still returns `200`
* Repeated logout remains successful
* Previous cookie value is not returned

## 22. Open API Decisions

| ID       | Decision                                                              | Status                   |
| -------- | --------------------------------------------------------------------- | ------------------------ |
| API-D001 | API prefix uses `/api/v1`                                             | Accepted                 |
| API-D002 | JSON is the primary request and response format                       | Accepted                 |
| API-D003 | JWT is delivered only through an HttpOnly cookie                      | Accepted                 |
| API-D004 | Logout is idempotent and returns `200`                                | Accepted                 |
| API-D005 | Registration does not automatically log in the user                   | Accepted                 |
| API-D006 | Health endpoint excludes database readiness in initial implementation | Accepted                 |
| API-D007 | Exact request-correlation identifier implementation                   | Deferred                 |
| API-D008 | Explicit CSRF-token endpoint                                          | Review before production |

## 23. API Completion Criteria

The Phase 1 API implementation will be complete when:

* All six endpoints are implemented.
* Request schemas match this document.
* Response schemas match this document.
* Status codes match this document.
* Authentication cookies are configured correctly.
* CORS supports only approved credentialed origins.
* Passwords and JWTs are not logged.
* API tests cover success and failure scenarios.
* OpenAPI documentation reflects the implementation.
* This document matches the final API behavior.
