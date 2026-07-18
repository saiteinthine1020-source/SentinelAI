# SentinelAI Phase 1 Authentication Flow

## 1. Document Information

| Item             | Value                        |
| ---------------- | ---------------------------- |
| Project          | SentinelAI                   |
| Document         | Phase 1 Authentication Flow  |
| Phase            | Phase 1 — Authentication MVP |
| Status           | Draft                        |
| Primary Language | English                      |
| Last Updated     | 2026-07-11                   |

## 2. Purpose

This document defines the authentication lifecycle for SentinelAI Phase 1.

It covers:

* User registration
* User login
* JWT creation
* HttpOnly cookie delivery
* Authenticated user retrieval
* Protected API access
* Protected frontend routes
* Authentication expiration
* Logout
* Authentication-related error handling

This document does not define refresh tokens, role-based access control, organization management, or external identity providers.

## 3. Authentication Design Summary

SentinelAI Phase 1 uses:

- Email and password authentication
- Secure password hashing
- JWT access tokens
- HttpOnly cookies
- Backend-enforced authentication
- Frontend route protection for user experience
- Short-lived access sessions
- Client-initiated logout

### 3.1 Core Authentication Decisions

- JWT `sub` claim stores the user UUID.
- Normalized lowercase email address is the Phase 1 login identifier.
- Plaintext passwords are never stored.
- Passwords are hashed using Argon2.
- Inactive accounts are rejected during authentication.

The backend remains the authoritative security boundary.

The frontend must never determine whether a user is authenticated only from local UI state.

## 4. Authentication Components

### 4.1 Frontend

The frontend is responsible for:

* Rendering registration and login forms
* Performing basic client-side validation
* Sending requests to the backend
* Sending cookies with credentialed requests using `withCredentials: true`
* Requesting the authenticated user
* Maintaining non-sensitive authentication state
* Protecting frontend routes
* Redirecting unauthenticated users
* Calling the logout endpoint
* Clearing local user state after logout

The frontend must not:

* Read the JWT directly
* Generate JWTs
* Hash passwords
* Store passwords
* Store database credentials
* Decide backend authorization

### 4.2 Backend

The backend is responsible for:

* Validating authentication requests
* Looking up users
* Hashing passwords
* Verifying passwords
* Generating JWTs
* Setting authentication cookies
* Validating authentication cookies
* Loading the authenticated user
* Rejecting unauthorized requests
* Clearing authentication cookies during logout
* Returning safe error messages

### 4.3 PostgreSQL

PostgreSQL is responsible for:

* Persisting users
* Enforcing email uniqueness
* Storing password hashes
* Storing user status
* Storing account timestamps

PostgreSQL must never store:

* Plaintext passwords
* JWT secrets
* Active JWT values

## 5. Registration Flow

### 5.1 User Action

The user opens the registration page and enters:

* Username
* Email address
* Password
* Password confirmation

### 5.2 Frontend Validation

The frontend performs basic validation:

* Required fields are present
* Email format appears valid
* Password confirmation matches
* Password meets the minimum UI rules

Frontend validation improves user experience but does not replace backend validation.

### 5.3 Registration Request

The frontend sends:

```http
POST /api/v1/auth/register
Content-Type: application/json
```

Example body:

```json
{
  "username": "sai",
  "email": "sai@example.com",
  "password": "ExamplePassword123!"
}
```

### 5.4 Backend Processing

The backend performs the following steps:

```text
1. Validate the request body.
2. Normalize the email address to lowercase.
3. Check whether the email already exists.
4. Validate password requirements.
5. Hash the password using Argon2.
6. Create the user record.
7. Commit the transaction.
8. Return a safe user response.
```
### 5.5 Password Policy

Phase 1 passwords must:

- Contain at least 12 characters
- Contain no more than 128 characters
- Include at least one uppercase letter
- Include at least one lowercase letter
- Include at least one number
- Include at least one special character

Passwords must be validated by the backend.

### 5.6 Registration Response

Successful registration should return:

```http
201 Created
```

Example:

```json
{
  "id": "user-identifier",
  "username": "sai",
  "email": "sai@example.com",
  "is_active": true,
  "created_at": "2026-07-11T10:00:00Z"
}
```

The response must not include:

* Password
* Password hash
* JWT secret
* Database information

### 5.7 Registration Error Cases

Possible errors:

```text
400 Bad Request
Invalid request format or password policy failure

409 Conflict
Email address already registered

422 Unprocessable Entity
Request validation failure

500 Internal Server Error
Unexpected backend failure
```

## 6. Login Flow

### 6.1 User Action

The user enters:

* Email address
* Password

### 6.2 Login Request

The frontend sends:

```http
POST /api/v1/auth/login
Content-Type: application/json
```

Example:

```json
{
  "email": "sai@example.com",
  "password": "ExamplePassword123!"
}
```

### 6.3 Backend Processing

The backend performs:

```text
1. Validate the request body.
2. Normalize the email address to lowercase.
3. Find the user by email.
4. Reject the request if the user is unavailable or inactive.
5. Verify the submitted password against the stored hash.
6. Create a JWT access token.
7. Set the JWT in an HttpOnly cookie.
8. Return a safe success response.
```

### 6.4 JWT Claims

The Phase 1 JWT should contain:

```json
{
  "sub": "user-identifier",
  "iat": 1783756800,
  "exp": 1783758600,
  "type": "access"
}
```

Claim meanings:

| Claim  | Meaning                       |
| ------ | ----------------------------- |
| `sub`  | Authenticated user identifier |
| `iat`  | Token issue time              |
| `exp`  | Token expiration time         |
| `type` | Token purpose                 |

The JWT must not contain:

* Password
* Password hash
* Full profile data
* Database credentials
* Secrets
* Sensitive company data

### 6.5 Authentication Cookie

Planned cookie name:

```text
sentinelai_access_token
```

Development configuration:

```text
HttpOnly = true
Secure = false
SameSite = Lax
Path = /
Max-Age = aligned with JWT expiration
```

Production configuration:

```text
HttpOnly = true
Secure = true
SameSite = Lax or stricter
Path = /
HTTPS required
```

### 6.6 Login Response

Successful login should return:

```http
200 OK
```

Example:

```json
{
  "message": "Login successful"
}
```

The JWT is delivered through the cookie, not the JSON response body.

### 6.7 Login Failure

Invalid credentials should return:

```http
401 Unauthorized
```

Example:

```json
{
  "detail": "Invalid email or password"
}
```

The backend should use the same error message whether:

* The email does not exist
* The password is incorrect

This reduces account-enumeration risk.

## 7. Authenticated User Flow

After successful login, the frontend requests the current user.

Request:

```http
GET /api/v1/auth/me
Cookie: sentinelai_access_token=<JWT>
```

The browser sends the cookie automatically when credentialed requests are enabled with `withCredentials: true`.

Backend processing:

```text
1. Read the authentication cookie.
2. Decode and verify the JWT.
3. Verify the token type.
4. Verify token expiration.
5. Read the user identifier from sub.
6. Retrieve the user.
7. Verify the user is active.
8. Return safe user information.
```

Successful response:

```http
200 OK
```

Example:

```json
{
  "id": "user-identifier",
  "username": "sai",
  "email": "sai@example.com",
  "is_active": true
}
```

## 8. Protected API Request Flow

Every protected request follows this pattern:

```text
Frontend request
    ↓
Browser includes HttpOnly cookie
    ↓
Backend reads cookie
    ↓
JWT signature validation
    ↓
Expiration validation
    ↓
Token type validation
    ↓
User lookup
    ↓
User status validation
    ↓
Protected response
```

If any validation fails, the request is rejected.

## 9. Protected Frontend Route Flow

The frontend dashboard route must not rely only on the existence of local user state.

Recommended behavior:

```text
1. User navigates to /dashboard.
2. Frontend checks whether authentication state is already loaded.
3. If not loaded, frontend calls GET /api/v1/auth/me.
4. If the request succeeds, the dashboard is shown.
5. If the request returns 401, the user is redirected to /login.
6. If the request fails unexpectedly, an error state is shown.
```

The frontend may cache safe user information in memory.

The frontend must not cache the JWT because the cookie is HttpOnly.

## 10. Session Expiration Flow

When the JWT expires:

```text
1. User sends a protected request.
2. Backend detects an expired token.
3. Backend returns 401 Unauthorized.
4. Frontend clears authenticated user state.
5. Frontend redirects the user to the login page.
6. User must log in again.
```

Phase 1 does not automatically refresh the session.

Refresh tokens may be added in a later phase.

## 11. Logout Flow

### 11.1 Logout Request

The frontend sends:

```http
POST /api/v1/auth/logout
```

The browser includes the authentication cookie.

### 11.2 Backend Processing

The backend clears the authentication cookie by returning the same cookie name with:

```text
Empty value
Expired date
Max-Age = 0
Matching Path
Matching Domain when applicable
```

### 11.3 Frontend Processing

After a successful logout response:

```text
1. Clear authenticated user state.
2. Clear cached non-sensitive session data.
3. Redirect to /login.
4. Prevent access to protected routes.
```

### 11.4 Important Limitation

The JWT remains cryptographically valid until it expires unless server-side revocation is implemented.

Phase 1 relies on:

* Short access-token lifetime
* Cookie deletion
* No refresh token
* Reauthentication after expiration

Token revocation may be introduced later.

## 12. Authentication Error Handling

### 12.1 Registration Errors

| Scenario                 | Status |
| ------------------------ | ------ |
| Invalid request          | 422    |
| Weak or invalid password | 400    |
| Duplicate email          | 409    |
| Unexpected error         | 500    |

### 12.2 Login Errors

| Scenario            | Status     |
| ------------------- | ---------- |
| Invalid credentials | 401        |
| Inactive user       | 403        |
| Invalid request     | 422        |
| Unexpected error    | 500        |

### 12.3 Authenticated Request Errors

| Scenario         | Status |
| ---------------- | ------ |
| Missing cookie   | 401    |
| Invalid JWT      | 401    |
| Expired JWT      | 401    |
| Wrong token type | 401    |
| User not found   | 401    |
| Inactive user    | 403    |

## 13. Security Rules

The implementation must follow these rules:

* Passwords must be hashed with Argon2.
* Plaintext passwords must never be stored.
* Plaintext passwords must never be logged.
* JWT values must never be logged.
* JWT secrets must come from environment variables.
* Authentication cookies must be HttpOnly.
* Production cookies must be Secure.
* CORS must allow only trusted frontend origins.
* Credentialed cross-origin requests must be explicitly configured.
* Login errors must not reveal account existence.
* Protected endpoints must validate authentication independently.
* Sensitive user fields must not be returned.
* Authentication code must have automated tests.

## 14. CSRF Consideration

Because authentication uses cookies, CSRF must be considered.

For Phase 1:

* `SameSite=Lax` provides baseline protection.
* CORS must restrict allowed origins.
* State-changing requests must not accept arbitrary cross-origin requests.
* Production deployment must use HTTPS.

Before introducing cross-site frontend hosting, refresh tokens, or more sensitive actions, SentinelAI should evaluate explicit CSRF tokens.

## 15. Authentication Sequence Diagram

### 15.1 Login

```text
User
  |
  | Enter email and password
  v
React Frontend
  |
  | POST /api/v1/auth/login
  v
FastAPI Backend
  |
  | Query user by email
  v
PostgreSQL
  |
  | Return user and password hash
  v
FastAPI Backend
  |
  | Verify password
  | Create JWT
  | Set HttpOnly cookie
  v
React Frontend
  |
  | GET /api/v1/auth/me
  v
FastAPI Backend
  |
  | Validate cookie and JWT
  | Load user
  v
PostgreSQL
  |
  | Return user
  v
React Frontend
  |
  | Show dashboard
  v
User
```

### 15.2 Protected Request

```text
React Frontend
  |
  | Request with cookie
  v
FastAPI Backend
  |
  | Validate JWT
  | Load current user
  v
Protected API Response
```

### 15.3 Logout

```text
User
  |
  | Click Logout
  v
React Frontend
  |
  | POST /api/v1/auth/logout
  v
FastAPI Backend
  |
  | Expire authentication cookie
  v
React Frontend
  |
  | Clear user state
  | Redirect to /login
```

## 16. Test Requirements

Authentication tests must cover:

* Successful registration
* Duplicate registration
* Invalid registration input
* Successful login
* Incorrect password
* Unknown email
* Inactive user
* Cookie creation
* Cookie security attributes
* Authenticated user retrieval
* Missing cookie
* Invalid JWT
* Expired JWT
* Wrong token type
* Logout cookie deletion
* Protected-route rejection after logout

## 17. Open Questions

| ID | Decision | Status |
|---|---|---|
| AUTH-001 | Access-token lifetime is 30 minutes | Accepted for Phase 1 |
| AUTH-002 | Inactive users receive `403 Forbidden` | Accepted |
| AUTH-003 | Phase 1 password policy requires 12–128 characters with uppercase, lowercase, numeric, and special characters | Accepted |
| AUTH-004 | Cookie domain configuration | Deferred until deployment |
| AUTH-005 | Explicit CSRF token requirement | Review before production |
## 18. Completion Criteria

This authentication-flow design is complete when:

* Registration flow is documented.
* Login flow is documented.
* JWT claims are defined.
* Cookie behavior is defined.
* Protected request behavior is defined.
* Session expiration is defined.
* Logout behavior is defined.
* Error cases are documented.
* Security rules are documented.
* Test requirements are documented.
* The design is aligned with the Basic Design and API Design documents.

## Implementation Status

Implemented:

* Email and password login
* Argon2 password verification
* Inactive-account rejection
* JWT access-token creation
* JWT `sub` claim containing the user UUID
* 30-minute token lifetime
* HttpOnly cookie delivery

Not yet implemented:

* `GET /api/v1/auth/me`
* Protected frontend routes
* Logout

