# SentinelAI Phase 1 Requirements

## 1. Document Information

| Item         | Value                |
| ------------ | -------------------- |
| Project      | SentinelAI           |
| Document     | Phase 1 Requirements |
| Phase        | Phase 1              |
| Status       | Draft                |
| Last Updated | 2026-07-10           |

## 2. Phase 1 Objective

The objective of Phase 1 is to build a secure authentication MVP.

This phase establishes the minimum technical foundation required for future user-specific features such as log storage, dashboards, reports, redaction settings, and AI analysis.

## 3. Functional Requirements

### FR-001: User Registration

The system shall allow a user to register using:

* Username
* Email address
* Password

Acceptance criteria:

* Username is required.
* Email is required.
* Password is required.
* Duplicate email addresses are rejected.
* Passwords are never stored in plain text.
* A successful registration returns an appropriate response.

### FR-002: User Login

The system shall allow a registered user to log in using:

* Email address
* Password

Acceptance criteria:

* Valid credentials return a JWT access token.
* Invalid credentials return an authentication error.
* The password is checked securely.

### FR-003: JWT Authentication

The backend shall protect private endpoints using JWT authentication.

Acceptance criteria:

* Valid tokens allow access.
* Missing tokens are rejected.
* Invalid tokens are rejected.
* Expired tokens are rejected.

### FR-004: Authenticated User Endpoint

The backend shall provide an endpoint that returns information about the currently authenticated user.

Acceptance criteria:

* The endpoint requires a valid token.
* The response does not expose the password hash.

### FR-005: Dashboard

The frontend shall provide a dashboard page for authenticated users.

Acceptance criteria:

* Unauthenticated users cannot access the dashboard.
* Authenticated users can see a welcome message.
* The dashboard can display basic user information.

### FR-006: Logout

The frontend shall provide a logout function.

Acceptance criteria:

* The stored access token is removed.
* The user is redirected to the login page.
* Protected pages are no longer accessible.

## 4. Non-Functional Requirements

### NFR-001: Security

* Passwords must be hashed using a secure password hashing algorithm.
* Secret values must be stored in environment variables.
* `.env` files must not be committed to GitHub.
* API responses must not expose password hashes.
* Input must be validated.
* Authentication errors should not reveal unnecessary information.

### NFR-002: Maintainability

* Backend code must be organized by responsibility.
* Frontend components must be organized clearly.
* Configuration must be separated from application logic.
* Database access must not be mixed directly into route handlers where avoidable.

### NFR-003: Testability

* Registration logic must have tests.
* Login logic must have tests.
* Protected endpoint behavior must have tests.
* Invalid authentication behavior must have tests.

### NFR-004: Development Environment

The local development environment shall use Docker Compose.

Planned services:

* Frontend
* Backend
* PostgreSQL

### NFR-005: Documentation

Phase 1 documentation must include:

* Basic Design
* Database Design
* API Design
* Screen Design
* Setup Guide
* Test Specification
* Release Notes

## 5. Constraints

* AWS is not used in Phase 1.
* AI is not used in Phase 1.
* Kubernetes is not used in Phase 1.
* Only one basic user role is supported.
* Refresh tokens may be postponed unless required by the final authentication design.
* The dashboard remains simple.

## 6. Out of Scope

The following are outside Phase 1:

* Log upload
* Log collection
* Log parsing
* Search and filtering
* Sensitive data redaction
* AI analysis
* Incident summaries
* Alerts
* Monitoring integrations
* Splunk integration
* Zabbix integration
* AWS deployment
* RBAC
* Organization management
* Audit logs
* API keys
* Billing
* SaaS multi-tenancy

## 7. Phase 1 Completion Criteria

Phase 1 is complete when:

* Users can register.
* Users can log in.
* JWT authentication works.
* Protected endpoints reject unauthenticated requests.
* Authenticated users can access the dashboard.
* Logout works.
* PostgreSQL stores user data.
* Docker Compose starts the required services.
* Required backend tests pass.
* Setup documentation is complete.
* Release notes are updated.
