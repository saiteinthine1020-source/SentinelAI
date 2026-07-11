# SentinelAI Phase 1 Basic Design

## 1. Document Information

| Item             | Value                        |
| ---------------- | ---------------------------- |
| Project          | SentinelAI                   |
| Document         | Phase 1 Basic Design         |
| Phase            | Phase 1 — Authentication MVP |
| Status           | Draft                        |
| Primary Language | English                      |
| Last Updated     | 2026-07-11                   |

## 2. Purpose

This document defines the basic system design for the SentinelAI Phase 1 Authentication MVP.

Phase 1 establishes the technical foundation required for future features such as log management, sensitive data redaction, AI-assisted analysis, dashboards, alerts, and monitoring.

This document covers only the architecture required for:

* User registration
* User login
* JWT authentication
* Authenticated user retrieval
* Protected dashboard access
* Logout
* PostgreSQL persistence
* Docker Compose-based local development

## 3. Scope

### 3.1 In Scope

* React frontend
* TypeScript
* Tailwind CSS
* FastAPI backend
* PostgreSQL database
* JWT access-token authentication
* Password hashing
* Docker Compose
* Environment-variable configuration
* Backend authentication tests

### 3.2 Out of Scope

The following are not included in Phase 1:

* Log collection
* Log upload
* Log search
* Sensitive data redaction
* AI integration
* Alerting
* Monitoring
* AWS deployment
* Kubernetes
* RBAC
* Organization management
* Audit logging
* Refresh-token rotation
* Multi-tenancy

## 4. High-Level Architecture

SentinelAI Phase 1 consists of three primary application services:

1. Frontend service
2. Backend service
3. PostgreSQL database service

```text
┌──────────────────────────────┐
│          Web Browser         │
└──────────────┬───────────────┘
               │ HTTP
               ▼
┌──────────────────────────────┐
│ React + TypeScript Frontend  │
│                              │
│ - Registration page          │
│ - Login page                 │
│ - Protected dashboard        │
│ - Authentication state       │
│ - Logout                     │
└──────────────┬───────────────┘
               │ REST API / JSON
               ▼
┌──────────────────────────────┐
│       FastAPI Backend        │
│                              │
│ - Request validation         │
│ - Registration logic         │
│ - Login logic                │
│ - Password hashing           │
│ - JWT creation               │
│ - JWT validation             │
│ - User retrieval             │
└──────────────┬───────────────┘
               │ SQL
               ▼
┌──────────────────────────────┐
│       PostgreSQL Database    │
│                              │
│ - User records               │
│ - Email uniqueness           │
│ - Password hashes            │
│ - Account timestamps         │
└──────────────────────────────┘
```

## 5. Component Responsibilities

### 5.1 Frontend

The frontend is responsible for:

* Rendering application screens
* Collecting registration and login input
* Validating basic form requirements
* Calling backend API endpoints
* Handling loading and error states
* Maintaining authenticated frontend state
* Sending the JWT with protected API requests
* Preventing unauthenticated dashboard access
* Removing authentication state during logout

The frontend must not:

* Hash passwords
* Generate JWTs
* Access PostgreSQL directly
* Store database credentials
* Make security decisions independently from the backend

### 5.2 Backend

The backend is responsible for:

* Validating API requests
* Applying authentication rules
* Hashing passwords
* Verifying passwords
* Creating JWT access tokens
* Validating JWT access tokens
* Retrieving the authenticated user
* Accessing PostgreSQL
* Returning safe API responses
* Preventing exposure of password hashes
* Producing consistent errors

The backend is the authoritative security boundary.

Frontend route protection improves user experience, but backend authentication determines whether access is permitted.

### 5.3 PostgreSQL

PostgreSQL is responsible for:

* Persisting user accounts
* Enforcing unique email addresses
* Storing password hashes
* Storing account status
* Storing creation and update timestamps
* Providing transactional consistency

PostgreSQL must not store plaintext passwords or JWT signing secrets.

### 5.4 Docker Compose

Docker Compose is responsible for:

* Starting the frontend service
* Starting the backend service
* Starting PostgreSQL
* Creating the internal service network
* Providing consistent local service names
* Mounting development volumes where appropriate
* Persisting PostgreSQL data
* Injecting non-committed environment configuration

## 6. Planned Service Structure

```text
services:
  frontend:
    responsibility: User interface
    communicates_with:
      - backend

  backend:
    responsibility: API and authentication logic
    communicates_with:
      - frontend
      - database

  database:
    responsibility: PostgreSQL persistence
    communicates_with:
      - backend
```

The frontend must not communicate directly with the database.

## 7. Authentication Design

### 7.1 Authentication Method

Phase 1 uses JWT access-token authentication.

The backend creates a signed JWT after successful login.

The JWT will contain only the minimum claims required to identify and validate the user session.

Planned claims:

* `sub`: authenticated user identifier
* `exp`: token expiration time
* `iat`: token creation time
* `type`: token type

Sensitive user data must not be placed inside the JWT.

### 7.2 Password Handling

Passwords follow this process:

```text
User password
    ↓
Backend validation
    ↓
Secure password hashing
    ↓
Password hash stored in PostgreSQL
```

During login:

```text
Submitted password
    ↓
Retrieve stored password hash
    ↓
Secure password verification
    ↓
Authentication success or failure
```

The original password must never be stored or logged.

### 7.3 Registration Flow

```text
1. User opens the registration page.
2. User enters username, email, and password.
3. Frontend performs basic form validation.
4. Frontend sends a registration request to the backend.
5. Backend validates the request.
6. Backend checks whether the email already exists.
7. Backend hashes the password.
8. Backend creates the user record.
9. Backend returns a safe user response.
10. Frontend redirects the user to the login page.
```

### 7.4 Login Flow

```text
1. User enters email and password.
2. Frontend sends credentials to the backend over HTTP.
3. Backend validates the request.
4. Backend retrieves the user by email.
5. Backend verifies the submitted password.
6. Backend creates a signed JWT access token.
7. Backend returns the access token.
8. Frontend stores the authentication state.
9. Frontend requests authenticated user information.
10. Frontend allows access to the dashboard.
```

### 7.5 Protected Request Flow

```text
1. Frontend prepares a protected API request.
2. Frontend includes the JWT in the Authorization header.
3. Backend extracts the bearer token.
4. Backend verifies the signature.
5. Backend verifies token expiration.
6. Backend reads the user identifier from the subject claim.
7. Backend retrieves the user.
8. Backend returns the protected response.
```

Header format:

```text
Authorization: Bearer <access-token>
```

### 7.6 Logout Flow

Phase 1 logout is client-side.

```text
1. User selects Logout.
2. Frontend removes the access token and authentication state.
3. Frontend redirects to the login page.
4. Protected frontend routes become inaccessible.
```

Phase 1 does not include server-side token revocation.

Server-side revocation, refresh-token rotation, and token denylisting may be evaluated in a later security-hardening phase.

## 8. Token Storage Decision

The final token storage mechanism must be confirmed before implementation.

Candidate approaches:

### Option A: Browser local storage

Advantages:

* Simple to implement
* Easy for an educational Phase 1 MVP

Risks:

* Tokens may be accessible to malicious JavaScript during an XSS attack

### Option B: Secure HttpOnly cookie

Advantages:

* JavaScript cannot directly read the token
* Better protection against token theft through XSS

Risks:

* Requires CSRF protection and more careful cookie configuration
* More complex local development behavior

### Initial Recommendation

Use an HttpOnly cookie-based authentication approach if the Phase 1 implementation can support it cleanly.

Use local storage only if the project explicitly accepts the security tradeoff for the first MVP and records the decision in an ADR.

The final decision must be documented before coding authentication.

## 9. Configuration Design

Sensitive and environment-specific configuration must be provided through environment variables.

Planned backend variables:

```text
APP_ENV
DATABASE_URL
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
CORS_ALLOWED_ORIGINS
```

Planned PostgreSQL variables:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

Planned frontend variables:

```text
VITE_API_BASE_URL
```

Rules:

* Real secrets must not be committed.
* `.env` must remain ignored by Git.
* `.env.example` will contain safe placeholders.
* Development and production values must remain separate.

## 10. API Communication

The frontend communicates with the backend using:

* HTTP
* REST-style endpoints
* JSON request and response bodies

The backend communicates with PostgreSQL using the approved Python database library and ORM layer.

Planned data flow:

```text
React form
    ↓ JSON
FastAPI request schema
    ↓ application service
Database repository
    ↓ SQL
PostgreSQL
```

Route handlers should remain thin.

Business logic and database access should be separated from API route definitions where practical.

## 11. Backend Layering

Recommended Phase 1 backend layers:

```text
API layer
    ↓
Service layer
    ↓
Repository or data-access layer
    ↓
PostgreSQL
```

Responsibilities:

### API Layer

* Route definitions
* Request parsing
* Response formatting
* Dependency injection
* HTTP status codes

### Service Layer

* Registration workflow
* Login workflow
* Authentication rules
* Business validation

### Repository Layer

* User lookup
* User creation
* Database queries

### Model and Schema Layer

* Database models
* Request schemas
* Response schemas

## 12. Error Handling

The backend should use consistent error responses.

Planned response structure:

```json
{
  "detail": "Error message"
}
```

Expected error categories:

* Validation error
* Duplicate email
* Invalid credentials
* Missing token
* Invalid token
* Expired token
* User not found
* Internal server error

Authentication errors must not reveal whether a particular email address exists unless required by the registration workflow.

## 13. Security Requirements

Phase 1 must follow these rules:

* Passwords must be hashed.
* Plaintext passwords must not be stored.
* Plaintext passwords must not be logged.
* JWT secrets must come from environment variables.
* Database credentials must not be committed.
* Password hashes must not appear in API responses.
* Protected endpoints must validate authentication.
* Request bodies must be validated.
* CORS must allow only approved frontend origins.
* Production secrets must differ from development values.
* Error messages must not expose internal implementation details.

## 14. Logging Requirements

Phase 1 application logs may include:

* Application startup
* Application shutdown
* Successful database connection
* Failed database connection
* Registration success without sensitive data
* Login success without tokens or passwords
* Authentication failure without submitted credentials
* Unexpected application errors

Logs must not contain:

* Passwords
* Password hashes
* JWTs
* Database passwords
* Full secret keys

## 15. Testing Strategy

Phase 1 backend tests should cover:

* Successful registration
* Duplicate email registration
* Invalid registration data
* Successful login
* Incorrect password
* Unknown user login
* Valid protected request
* Missing token
* Invalid token
* Expired token
* Safe authenticated-user response

Testing should use isolated test data.

Tests must not depend on production services or production credentials.

## 16. Deployment Boundary

Phase 1 is designed for local development using Docker Compose.

AWS deployment is explicitly deferred until Phase 7.

The Phase 1 design should still avoid decisions that would make future deployment unnecessarily difficult.

## 17. Future Extension Points

The architecture should allow future addition of:

* Log ownership
* Redaction settings
* Organization membership
* Roles and permissions
* Audit logs
* API keys
* Refresh tokens
* External identity providers
* AI-provider configuration

These features must not be implemented during Phase 1.

## 18. Open Design Decisions

The following decisions require confirmation before implementation:

| ID     | Decision                                                                     | Status |
| ------ | ---------------------------------------------------------------------------- | ------ |
DD-001 | JWT transport using HttpOnly cookie | Accepted in ADR-001
| DD-002 | Backend ORM and migration tooling                                            | Open   |
| DD-003 | Password hashing algorithm and library                                       | Open   |
| DD-004 | Python dependency-management approach                                        | Open   |
| DD-005 | Frontend API client strategy                                                 | Open   |

Important decisions should be documented using Architecture Decision Records.

## 19. Phase 1 Basic Design Completion Criteria

This document is complete when:

* Component responsibilities are defined.
* Authentication flows are documented.
* Configuration rules are documented.
* Security boundaries are clear.
* Backend layers are defined.
* Open architectural decisions are identified.
* Database, API, and screen design documents are aligned.
* No out-of-scope feature is included.
