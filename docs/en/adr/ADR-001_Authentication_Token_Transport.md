# ADR-001: Authentication Token Transport

## Status

Accepted

## Date

2026-07-11

## Context

SentinelAI Phase 1 requires JWT-based authentication between the React frontend and FastAPI backend.

The access token must be transported and stored in a way that balances security, maintainability, and implementation complexity.

The main options considered were:

1. Store the JWT in browser local storage and send it through the Authorization header.
2. Store the JWT in an HttpOnly cookie managed by the backend.

## Decision

SentinelAI Phase 1 will use an HttpOnly cookie for the JWT access token.

The backend will create the JWT and return it using a cookie configured with appropriate security attributes.

Planned development configuration:

* `HttpOnly=true`
* `SameSite=Lax`
* `Secure=false` for local HTTP development
* Restricted cookie path
* Explicit expiration

Planned production configuration:

* `HttpOnly=true`
* `SameSite=Lax` or stricter based on deployment requirements
* `Secure=true`
* HTTPS only
* Restricted domain and path settings

The frontend will send credentialed requests to the backend.

## Consequences

### Positive

* Frontend JavaScript cannot directly read the JWT.
* The risk of JWT theft through XSS is reduced.
* Authentication handling is centralized in the backend.
* The design is closer to production security practices.

### Negative

* CORS must support credentialed requests.
* Cookie attributes must differ between local and production environments.
* CSRF risks must be considered.
* Frontend requests must enable credentials.
* Testing is more complex than basic local-storage authentication.

## Security Notes

HttpOnly cookies do not eliminate all authentication risks.

The implementation must also include:

* Restricted CORS origins
* Appropriate SameSite settings
* CSRF evaluation
* Short token expiration
* Secure cookies in production
* Protection against cross-site scripting
* Safe logout behavior

## Alternatives Rejected

### Browser Local Storage

Local storage is easier to implement, but JavaScript can read the token. A successful XSS attack could expose it.

This tradeoff was rejected because SentinelAI is intended to demonstrate secure engineering practices.

## Review Condition

This decision should be reviewed before:

* Introducing refresh tokens
* Deploying to AWS
* Supporting multiple frontend domains
* Adding external identity providers
* Implementing multi-tenant SaaS authentication
