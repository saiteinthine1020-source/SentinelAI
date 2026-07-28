# SentinelAI Phase 1 Setup Guide

## 1. Purpose

This guide explains how to build, run, test, and verify the SentinelAI Phase 1 Authentication MVP locally.

Phase 1 includes:

* React and TypeScript frontend
* FastAPI backend
* PostgreSQL database
* Docker Compose development environment
* User registration
* User login
* JWT authentication through an HttpOnly cookie
* Current-user session verification
* Protected dashboard
* Logout
* Backend authentication tests

## 2. Prerequisites

Required software:

* Git
* Docker Desktop
* Docker Compose
* Visual Studio Code or another editor
* A modern web browser

Verify Docker:

```powershell
docker --version
docker compose version
docker info
```

Docker Desktop must be running.

## 3. Clone the Repository

```powershell
git clone https://github.com/saiteinthine1020-source/SentinelAI.git
cd SentinelAI
```

## 4. Create the Local Environment File

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder development values.

Required values include:

```dotenv
POSTGRES_DB=sentinelai
POSTGRES_USER=sentinelai
POSTGRES_PASSWORD=<local-development-password>

DATABASE_URL=postgresql+psycopg://sentinelai:<local-development-password>@database:5432/sentinelai

JWT_SECRET_KEY=<long-random-local-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ACCESS_TOKEN_COOKIE_NAME=sentinelai_access_token
COOKIE_SECURE=false
COOKIE_SAMESITE=lax
COOKIE_PATH=/

CORS_ALLOWED_ORIGINS=http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000
```

The `.env` file contains local secrets and must never be committed.

Verify that Git ignores it:

```powershell
git check-ignore .env
```

Expected:

```text
.env
```

## 5. Validate Docker Compose

```powershell
docker compose config
```

The resolved output may contain environment values. Do not publish it if it contains local secrets.

## 6. Build the Services

```powershell
docker compose build
```

This builds:

* SentinelAI frontend image
* SentinelAI backend image

PostgreSQL uses the official container image.

## 7. Start the Services

```powershell
docker compose up -d
```

Check status:

```powershell
docker compose ps
```

Expected services:

* `sentinelai-database`
* `sentinelai-backend`
* `sentinelai-frontend`

The database and backend should become healthy.

## 8. Apply Database Migrations

```powershell
docker compose run --rm backend alembic upgrade head
```

Check the current migration:

```powershell
docker compose run --rm backend alembic current
```

Check the latest migration head:

```powershell
docker compose run --rm backend alembic heads
```

The current revision should match the migration head.

## 9. Verify Backend Health

Basic process health:

```powershell
curl.exe http://localhost:8000/health
```

Expected:

```json
{
  "status": "ok",
  "service": "sentinelai-backend",
  "version": "0.1.0",
  "environment": "development"
}
```

Database readiness:

```powershell
curl.exe http://localhost:8000/health/ready
```

Expected:

```json
{
  "status": "ready",
  "database": "available"
}
```

## 10. Access the Application

Frontend:

```text
http://localhost:5173
```

Login:

```text
http://localhost:5173/login
```

Registration:

```text
http://localhost:5173/register
```

Protected dashboard:

```text
http://localhost:5173/dashboard
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

## 11. Register a User

Use the browser registration page or PowerShell:

```powershell
$registrationBody = @{
    username = "example_user"
    email = "example.user@example.com"
    password = "StrongPassword123!"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/api/v1/auth/register" `
    -ContentType "application/json" `
    -Body $registrationBody
```

Expected status:

```text
201 Created
```

The response contains safe public user data and does not contain the password or password hash.

## 12. Log In

```powershell
$loginBody = @{
    email = "example.user@example.com"
    password = "StrongPassword123!"
} | ConvertTo-Json

$loginResponse = Invoke-WebRequest `
    -Method Post `
    -Uri "http://localhost:8000/api/v1/auth/login" `
    -ContentType "application/json" `
    -Body $loginBody `
    -SessionVariable authenticationSession

$loginResponse.StatusCode
$loginResponse.Content
```

Expected body:

```json
{
  "message": "Login successful"
}
```

The access token is delivered through the `sentinelai_access_token` HttpOnly cookie.

Do not print or publish the complete cookie value.

## 13. Verify the Current User

Use the session created during login:

```powershell
Invoke-RestMethod `
    -Method Get `
    -Uri "http://localhost:8000/api/v1/auth/me" `
    -WebSession $authenticationSession
```

Expected response:

```json
{
  "id": "user-uuid",
  "username": "example_user",
  "email": "example.user@example.com",
  "is_active": true,
  "created_at": "ISO-8601 timestamp"
}
```

A request without a valid cookie returns:

```text
401 Unauthorized
```

## 14. Log Out

```powershell
Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/api/v1/auth/logout" `
    -WebSession $authenticationSession
```

Expected:

```json
{
  "message": "Logout successful"
}
```

Logout is idempotent and succeeds even when the authentication cookie is missing or invalid.

## 15. Run Backend Quality Checks

Lint:

```powershell
docker compose run --rm backend ruff check app tests alembic
```

Formatting:

```powershell
docker compose run --rm backend ruff format --check app tests alembic
```

Tests:

```powershell
docker compose run --rm backend pytest
```

Verbose tests:

```powershell
docker compose run --rm backend pytest -v
```

Coverage:

```powershell
docker compose run --rm backend pytest `
    --cov=app `
    --cov-report=term-missing
```

## 16. Run Frontend Quality Checks

TypeScript:

```powershell
docker compose run --rm frontend npm run typecheck
```

Lint:

```powershell
docker compose run --rm frontend npm run lint
```

Production build:

```powershell
docker compose run --rm frontend npm run build
```

## 17. View Logs

All services:

```powershell
docker compose logs
```

Backend:

```powershell
docker compose logs -f backend
```

Frontend:

```powershell
docker compose logs -f frontend
```

Database:

```powershell
docker compose logs -f database
```

Press `Ctrl+C` to stop following logs. This does not stop the containers.

## 18. Open PostgreSQL

```powershell
docker compose exec database psql -U sentinelai -d sentinelai
```

List tables:

```text
\dt
```

Inspect the `users` table:

```text
\d users
```

Exit:

```text
\q
```

Do not print full password hashes or credentials in documentation.

## 19. Stop the Environment

Stop containers while preserving PostgreSQL data:

```powershell
docker compose down
```

Restart:

```powershell
docker compose up -d
```

## 20. Reset Local Database Data

Use only when intentionally deleting local PostgreSQL data:

```powershell
docker compose down -v
```

Then rebuild and migrate:

```powershell
docker compose up -d database
docker compose run --rm backend alembic upgrade head
docker compose up -d
```

The `-v` option deletes named volumes.

## 21. Rebuild After Dependency Changes

Backend:

```powershell
docker compose build backend
```

Frontend:

```powershell
docker compose build frontend
```

All services:

```powershell
docker compose build
```

For a clean rebuild:

```powershell
docker compose build --no-cache
```

Use `--no-cache` only when a normal rebuild does not resolve the problem.

## 22. Troubleshooting

### Docker daemon is unavailable

Open Docker Desktop and retry:

```powershell
docker info
```

### Port is already in use

SentinelAI uses:

* Frontend: `5173`
* Backend: `8000`
* PostgreSQL: `5432`

Stop the conflicting process or update the local port mapping.

### Backend cannot connect to PostgreSQL

Confirm:

* PostgreSQL is healthy.
* `DATABASE_URL` uses `database` as the hostname.
* PostgreSQL credentials match.
* `.env` exists.
* Migrations have been applied.

### Backend returns database unavailable

Check:

```powershell
docker compose ps
docker compose logs database
docker compose logs backend
```

### Frontend cannot reach the backend

Confirm:

```dotenv
VITE_API_BASE_URL=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Rebuild the frontend after environment changes.

### Login succeeds but dashboard redirects to login

Check:

* Browser cookies are enabled.
* The login response contains `Set-Cookie`.
* Frontend requests use credentials.
* Backend CORS allows the exact frontend origin.
* `/api/v1/auth/me` returns `200`.

### Migration is not current

Run:

```powershell
docker compose run --rm backend alembic upgrade head
docker compose run --rm backend alembic current
docker compose run --rm backend alembic heads
```

## 23. Security Notes

* Never commit `.env`.
* Never store JWTs in local storage or session storage.
* Never expose `JWT_SECRET_KEY` to the frontend.
* Never log passwords, password hashes, JWTs, or cookie values.
* Development uses `COOKIE_SECURE=false`.
* Production must use HTTPS and `COOKIE_SECURE=true`.
* Frontend validation does not replace backend validation.
* PostgreSQL unique constraints remain the final duplicate-user protection.
* Generated Alembic migrations must be reviewed before execution.
