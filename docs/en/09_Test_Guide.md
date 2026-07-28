# SentinelAI Phase 1 Test Guide

## Authentication Test Scope

The Phase 1 backend test suite covers:

* User registration
* Username normalization
* Email normalization
* Password-policy validation
* Argon2 password hashing
* Duplicate email rejection
* Duplicate username rejection
* User login
* Generic invalid-credential responses
* Inactive-account rejection
* JWT creation
* JWT signature validation
* JWT expiration validation
* JWT token-type validation
* Current-user retrieval
* Missing-cookie handling
* Invalid-cookie handling
* Unknown-user handling
* Logout
* Idempotent logout
* Sensitive-field exclusion
* Complete authentication flow

## Run Backend Tests

```powershell
docker compose up -d database
docker compose run --rm backend alembic upgrade head
docker compose run --rm backend pytest
```
