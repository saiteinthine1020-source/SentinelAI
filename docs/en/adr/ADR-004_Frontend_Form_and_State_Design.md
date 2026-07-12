# ADR-004: Frontend Form and Authentication State Design

## Status

Accepted

## Date

2026-07-12

## Context

SentinelAI Phase 1 requires registration and login forms, frontend validation, API communication, and authenticated-user state.

The frontend must support:

* Type-safe forms
* Clear validation errors
* Credentialed API requests
* Protected routes
* Authentication loading states
* Safe user-state management
* Maintainable separation between UI and API logic

The JWT is stored in an HttpOnly cookie and cannot be read by frontend JavaScript.

## Decision

SentinelAI Phase 1 will use:

* React Hook Form for form-state management
* Zod for frontend validation schemas
* Axios for centralized API communication
* In-memory React authentication state for safe public user data
* Backend session verification through `GET /api/v1/auth/me`
* Credentialed API requests
* Route guards based on verified authentication state

The frontend will not store the JWT.

## Form Design

React Hook Form will manage:

* Input values
* Field errors
* Submit state
* Form validation integration
* Duplicate-submission prevention

Zod will define client-side schemas for:

* Registration
* Login

Frontend validation improves user experience but does not replace backend validation.

## API Client Design

Axios will be configured once in a centralized client.

Conceptual configuration:

```typescript
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json"
  }
});
```

Components should not recreate API configuration independently.

## Authentication State

The frontend stores only safe public user information.

Conceptual state:

```typescript
type AuthState =
  | { status: "loading"; user: null }
  | { status: "authenticated"; user: PublicUser }
  | { status: "unauthenticated"; user: null }
  | { status: "error"; user: null };
```

The frontend must not store:

* JWT values
* Passwords
* Password hashes
* Cookie values
* Backend secrets

## Session Verification

When the application starts or a protected route is opened:

1. The frontend calls `GET /api/v1/auth/me`.
2. The browser sends the HttpOnly cookie.
3. The backend validates the session.
4. The frontend stores the returned public user data.
5. The application renders the correct route.

The frontend does not infer authentication from the presence of local data alone.

## Consequences

### Positive

* Form logic remains organized.
* Validation schemas are reusable and type-safe.
* API configuration is centralized.
* JWT values remain inaccessible to frontend JavaScript.
* Protected-route behavior is consistent.
* Authentication state is explicit.
* Components remain easier to test.

### Negative

* The frontend introduces additional dependencies.
* Authentication verification requires an API request on application startup.
* Route loading states must be handled carefully.
* Backend and frontend validation rules must remain synchronized.
* Axios interceptors must not create redirect loops.

## Alternatives Considered

### Native React State Only

Possible for simple forms, but larger forms become repetitive and harder to validate consistently.

### Formik

Formik is mature, but React Hook Form is generally lighter and aligns well with schema-based validation.

### Fetch API

The native Fetch API is sufficient, but Axios provides convenient centralized configuration and consistent credential handling for this project.

### Local Storage Authentication State

Local storage survives page reloads, but it can become stale and must not be used to store the JWT.

The backend session remains authoritative.

## Rules

* The JWT must never be stored in local storage or session storage.
* Frontend validation must not be treated as a security boundary.
* All authentication API requests must include credentials.
* `401` responses must clear authenticated user state.
* `403` responses for inactive users must clear authenticated user state.
* Components must not log passwords or full authentication payloads.
* API configuration must be centralized.
* Protected-route guards must handle loading before redirecting.

## Review Conditions

Review this ADR before:

* Introducing refresh tokens
* Adding global state-management libraries
* Adding complex dashboard state
* Supporting multiple frontend applications
* Introducing external identity providers
* Adding offline authentication behavior
