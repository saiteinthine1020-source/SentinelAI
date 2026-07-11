# ADR-003: Phase 1 API Conventions

## Status

Accepted

## Date

2026-07-11

## Context

SentinelAI requires a consistent API contract between the React frontend and FastAPI backend.

The project needs conventions for:

* API versioning
* Endpoint naming
* JSON communication
* Authentication transport
* Error responses
* Status-code usage
* Logout behavior

Without explicit conventions, endpoint behavior may become inconsistent as the application grows.

## Decision

SentinelAI Phase 1 will use:

* REST-style HTTP endpoints
* JSON request and response bodies
* `/api/v1` as the business API prefix
* Noun- and action-oriented authentication routes under `/auth`
* FastAPI-compatible `detail` error responses
* JWT authentication through an HttpOnly cookie
* Credentialed frontend requests
* Idempotent logout behavior

## Endpoint Conventions

Phase 1 endpoints:

```text
GET  /health
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
POST /api/v1/auth/logout
```

## Status-Code Conventions

* `200 OK` for successful reads and actions
* `201 Created` for user registration
* `400 Bad Request` for business-rule validation failures
* `401 Unauthorized` for missing or invalid authentication
* `403 Forbidden` for inactive-user access
* `409 Conflict` for duplicate unique resources
* `422 Unprocessable Entity` for schema validation
* `500 Internal Server Error` for unexpected failures

## Error Convention

Application errors should use:

```json
{
  "detail": "Error message"
}
```

Schema-validation errors may use FastAPI's standard structured validation format.

## Authentication Convention

The backend stores the JWT access token in an HttpOnly cookie.

The frontend must send credentialed requests.

The JWT must not be returned in JSON.

## Logout Convention

Logout is idempotent.

The endpoint should return success even when:

* The cookie is missing
* The cookie is expired
* Logout is requested repeatedly

The backend clears the authentication cookie and the frontend clears local user state.

## Consequences

### Positive

* Frontend and backend responsibilities are clear.
* API behavior is predictable.
* Status codes are consistent.
* Authentication transport remains centralized.
* Future OpenAPI documentation can reflect a stable contract.
* API tests can be written against explicit behavior.

### Negative

* Cookie-based authentication requires credentialed CORS configuration.
* CSRF considerations remain necessary.
* Versioning introduces a longer endpoint prefix.
* Custom business errors require consistent backend handling.

## Alternatives Considered

### Unversioned API Paths

Unversioned paths are simpler initially but make future breaking changes harder to manage.

### JWT in JSON Response

Returning the JWT in JSON is common in simple tutorials, but it encourages frontend-accessible token storage.

This was rejected in favor of HttpOnly cookies.

### Always Returning `200`

Using `200` for all outcomes simplifies client parsing but weakens HTTP semantics and monitoring clarity.

This was rejected.

## Review Conditions

Review this ADR before:

* Adding refresh tokens
* Introducing API keys
* Supporting external clients
* Adding organization-scoped APIs
* Publishing a public API
* Introducing GraphQL
* Deploying frontend and backend across different sites
