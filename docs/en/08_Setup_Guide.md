# SentinelAI Phase 1 Setup Guide

## 1. Purpose

This guide documents the development foundation that is currently present in the SentinelAI repository, explains what each part is for, and shows how to run it locally.

Phase 1 currently provides a containerized React frontend, FastAPI backend, and PostgreSQL database. It verifies that the three-service development environment can start successfully. It does not yet provide the planned authentication or application features.

## 2. What Is Currently Set Up

| Component | Current setup | Purpose |
| --- | --- | --- |
| Frontend | React 19, TypeScript 6, Vite 8, and Oxlint on Node.js 22 | Provides the browser user interface and development server |
| Backend | Python 3.12, FastAPI, and Uvicorn | Provides the HTTP API and interactive API documentation |
| Database | PostgreSQL 17 Alpine | Provides persistent relational data storage for later backend features |
| Database libraries | SQLAlchemy 2 and Psycopg 3 | Prepare the backend for future database access |
| Backend development tools | Pytest, HTTPX, and Ruff | Support testing, API test clients, linting, and formatting checks |
| Containers | Docker Desktop and Docker Compose | Build and run the frontend, backend, and database consistently |
| Configuration | `.env.example` and a local `.env` | Supply Compose and application settings without committing local secrets |

### Current implementation boundary

The following facts describe the repository as it exists now:

* The frontend displays a Phase 1 environment status card.
* The frontend does not yet call the backend API.
* Axios, React Hook Form, Zod, and Tailwind CSS are not installed yet.
* The backend currently exposes `GET /health`, `/docs`, and the automatically generated OpenAPI endpoints.
* The backend does not yet define database models, migrations, repositories, or authentication routes.
* PostgreSQL is running and its connection URL is supplied to the backend, but the current health endpoint does not query it.
* JWT and CORS values are available as environment variables, but the application does not yet use them.

These planned capabilities belong to later frontend initialization, database, and authentication work.

## 3. Repository Structure

```text
SentinelAI/
|-- backend/
|   |-- app/
|   |   |-- __init__.py
|   |   `-- main.py
|   |-- Dockerfile
|   `-- pyproject.toml
|-- frontend/
|   |-- src/
|   |-- Dockerfile
|   |-- package.json
|   `-- vite.config.ts
|-- docs/
|-- .env.example
`-- docker-compose.yml
```

## 4. Prerequisites

Required:

* Git
* Docker Desktop with the Linux container engine running
* Docker Compose, included with current Docker Desktop releases
* A modern web browser
* Visual Studio Code or another code editor

Node.js and Python are not required on the host for the Docker-based workflow. They are only needed if the frontend or backend is run directly outside Docker.

Verify Docker before continuing:

```powershell
docker version
docker compose version
```

Both commands must show their client information, and `docker version` must also show a server section.

## 5. Clone the Repository

```powershell
git clone https://github.com/saiteinthine1020-source/SentinelAI.git
cd SentinelAI
```

Run all remaining commands from the repository root.

## 6. Configure Environment Variables

Create the local environment file from the committed template:

```powershell
Copy-Item .env.example .env
```

Change the placeholder password and JWT secret in `.env` before using the environment beyond local development. The `.env` file contains local secrets and must not be committed.

### Environment variables

| Variable | Used for |
| --- | --- |
| `APP_ENV` | Identifies the application environment |
| `POSTGRES_DB` | Creates the initial PostgreSQL database |
| `POSTGRES_USER` | Creates the PostgreSQL application user |
| `POSTGRES_PASSWORD` | Sets the PostgreSQL application-user password |
| `DATABASE_URL` | Gives the backend its PostgreSQL connection string |
| `JWT_SECRET_KEY` | Reserved for signing authentication tokens later |
| `JWT_ALGORITHM` | Reserved for the JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Reserved for access-token lifetime configuration |
| `CORS_ALLOWED_ORIGINS` | Reserved for backend CORS configuration |
| `VITE_API_BASE_URL` | Gives the frontend the intended backend base URL |

The PostgreSQL credentials in `DATABASE_URL` must match `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`.

## 7. Understand the Database Hostname

The backend runs inside a container, so its database hostname must be the Compose service name:

```text
database:5432
```

The current URL therefore contains:

```text
@database:5432
```

Inside the backend container, `localhost` means the backend container itself. Docker Compose resolves `database` to the PostgreSQL container because both services are attached to `sentinelai-network`.

From Windows host tools, PostgreSQL is reached through its published address:

```text
localhost:5432
```

## 8. Validate the Compose Configuration

```powershell
docker compose config
```

This expands the Compose file and substitutes values from `.env`. Treat the output as potentially sensitive because it can contain resolved credentials.

## 9. Build and Start the Environment

Build the local frontend and backend images:

```powershell
docker compose build
```

Start all three services in the background:

```powershell
docker compose up -d
```

Compose starts PostgreSQL first and waits for its health check before starting the backend. The frontend declares a dependency on the backend.

Check container status:

```powershell
docker compose ps
```

The expected services are:

* `database` / `sentinelai-database`
* `backend` / `sentinelai-backend`
* `frontend` / `sentinelai-frontend`

## Backend Quality Checks

Run backend linting:

```powershell
docker compose run --rm backend ruff check app tests
```

## Database and Migration Commands

Start PostgreSQL:

```powershell
docker compose up -d database
```

Check PostgreSQL health:

```powershell
docker compose ps
```

Show the current migration revision:

```powershell
docker compose run --rm backend alembic current
```

Show the latest migration head:

```powershell
docker compose run --rm backend alembic heads
```

Apply all migrations:

```powershell
docker compose run --rm backend alembic upgrade head
```

Revert one migration:

```powershell
docker compose run --rm backend alembic downgrade -1
```

Create a migration after changing SQLAlchemy models:

```powershell
docker compose run --rm backend alembic revision --autogenerate -m "describe schema change"
```

Generated migrations must be reviewed before they are applied.

Check for model changes that do not yet have a migration:

```powershell
docker compose run --rm backend alembic check
```

Open PostgreSQL:

```powershell
docker compose exec database psql -U sentinelai -d sentinelai
```

Inside PostgreSQL, list tables:

```text
\dt
```

Exit PostgreSQL:

```text
\q
```

Database readiness endpoint:

```text
http://localhost:8000/health/ready
```

## Frontend Development Commands

Build the frontend Docker image:

```powershell
docker compose build frontend
```

Run frontend linting:

```powershell
docker compose run --rm frontend npm run lint
```

Run TypeScript checks:

```powershell
docker compose run --rm frontend npm run typecheck
```

Create a production build:

```powershell
docker compose run --rm frontend npm run build
```

Start the frontend development server:

```powershell
docker compose up -d frontend
```

Open the frontend:

```text
http://localhost:5173
```

Phase 1 routes:

```text
/login
/register
/dashboard
```

The dashboard route is not protected until the authentication feature is implemented.

## 10. Access the Services

| Service | Address | Current result |
| --- | --- | --- |
| Frontend | `http://localhost:5173` | React Phase 1 status page |
| Backend health | `http://localhost:8000/health` | Basic backend process response |
| FastAPI documentation | `http://localhost:8000/docs` | Interactive Swagger UI |
| OpenAPI schema | `http://localhost:8000/openapi.json` | Generated API specification |
| PostgreSQL | `localhost:5432` | Host connection for database tools |

The `/health` endpoint confirms that FastAPI is responding. Use `/health/ready` to check PostgreSQL readiness.

## Test User Registration

Open:

```text
http://localhost:5173/register
```

Or use PowerShell:

```powershell
$body = @{
    username = "example_user"
    email = "example.user@example.com"
    password = "StrongPassword123!"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/api/v1/auth/register" `
    -ContentType "application/json" `
    -Body $body
```

## 11. Development Mounts and Persistence

The backend mounts `backend/app` and `backend/tests` into its container. Uvicorn runs with `--reload`, so Python application changes are reloaded during development.

The frontend mounts the `frontend` directory into its container. Vite listens on `0.0.0.0:5173`, making the development server accessible from the host browser. A named volume keeps container-installed `node_modules` separate from the host source tree.

PostgreSQL stores its data in the `sentinelai_postgres_data` named volume. A normal container restart or `docker compose down` does not delete this data.

## 12. View Logs

All services:

```powershell
docker compose logs
```

Follow one service in real time:

```powershell
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f database
```

Press `Ctrl+C` to stop following logs. This does not stop the containers.

## 13. Stop or Reset the Environment

Stop and remove the development containers while keeping named-volume data:

```powershell
docker compose down
```

Restart existing services:

```powershell
docker compose restart
```

Delete the PostgreSQL data and frontend dependency volumes only when an intentional full reset is required:

```powershell
docker compose down -v
```

The `-v` command permanently removes the Compose named volumes, including local PostgreSQL data.

## 14. Rebuild After Dependency Changes

Rebuild after changing `backend/pyproject.toml`, `frontend/package.json`, either Dockerfile, or other image-build inputs:

```powershell
docker compose up -d --build
```

Use a cache-free rebuild only when a normal rebuild does not apply the expected changes:

```powershell
docker compose build --no-cache
docker compose up -d
```

## 15. Optional Host-Side Commands

These commands are not required for the Docker workflow. Use them only when Node.js or Python is intentionally installed on the host.

Frontend dependency installation and checks:

```powershell
cd frontend
npm.cmd install
npm.cmd run lint
npm.cmd run build
cd ..
```

`npm.cmd` avoids the PowerShell execution-policy error that can occur when PowerShell blocks `npm.ps1`.

## 16. Troubleshooting

### Docker Desktop does not show a window

Docker Desktop can continue running in the Windows system tray without an open dashboard. Check the engine directly:

```powershell
docker version
docker info
```

If the client works but no server information is shown, start or restart Docker Desktop and wait for the Linux engine to become ready.

### Image download fails with `EOF`

An `EOF` from Docker Hub or CloudFront usually means the image download was interrupted. Retry:

```powershell
docker compose pull
docker compose up -d --build
```

If it repeats, restart Docker Desktop and check the network, VPN, proxy, firewall, and Docker Hub connectivity. This error is normally unrelated to the Compose service definitions.

### `docker` is not recognized

Restart the terminal or Visual Studio Code after installing or updating Docker Desktop so the process receives the updated `PATH`. Then retry `docker version`.

### PowerShell blocks `npm.ps1`

Use the Windows command wrapper:

```powershell
npm.cmd install
npm.cmd run dev
```

### Port already in use

Another process may already be using port `5173`, `8000`, or `5432`. Stop that process or change the relevant host-side port mapping in `docker-compose.yml`.

### Backend cannot connect to PostgreSQL

Confirm that:

* The database container is healthy.
* `DATABASE_URL` uses `database`, not `localhost`, as its container-side hostname.
* The PostgreSQL credentials in `.env` and `DATABASE_URL` match.
* The `.env` file exists in the repository root.
* The backend and database are attached to `sentinelai-network`.

Inspect the relevant logs:

```powershell
docker compose logs backend
docker compose logs database
```

### Environment variable changes do not apply

Recreate the containers so Compose supplies the new values:

```powershell
docker compose down
docker compose up -d --build
```
