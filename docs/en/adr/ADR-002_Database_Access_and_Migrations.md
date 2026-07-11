# ADR-002: Database Access and Migration Tooling

## Status

Accepted

## Date

2026-07-11

## Context

SentinelAI requires a maintainable method for accessing PostgreSQL and managing schema changes.

The Phase 1 Authentication MVP needs:

* User persistence
* Unique constraints
* Transaction management
* Database testing
* Repeatable schema creation
* Future schema evolution

Direct SQL could be used, but the project is intended to demonstrate maintainable application architecture and long-term database evolution.

## Decision

SentinelAI will use:

* SQLAlchemy 2.x for database models and database access
* Alembic for version-controlled database migrations

The backend will use SQLAlchemy's modern 2.x API.

Database schema changes will be introduced through Alembic migration files.

## Rationale

SQLAlchemy provides:

* Mature PostgreSQL support
* Explicit transaction handling
* Model definitions
* Query construction
* Dependency-injection compatibility
* Strong integration with FastAPI
* Support for future repository-layer abstractions

Alembic provides:

* Version-controlled schema history
* Upgrade and downgrade paths
* Repeatable environment setup
* Reviewable database changes
* Integration with SQLAlchemy metadata

## Consequences

### Positive

* Database changes are traceable.
* Local and future production schemas can remain aligned.
* Database access can be separated from route handlers.
* Tests can use consistent database models.
* Future tables can be introduced incrementally.

### Negative

* The project requires additional configuration.
* Developers must understand migrations.
* ORM behavior can hide inefficient queries if used carelessly.
* Migration files require review and maintenance.

## Rules

* Application startup must not recreate the full schema automatically in production.
* Alembic migrations must be committed.
* Database sessions must be closed correctly.
* Route handlers should not contain complex database logic.
* Public response schemas must remain separate from ORM models.
* Migration history must not be modified casually after it is shared.

## Alternatives Considered

### Raw SQL Only

Raw SQL provides direct control but would require more manual mapping, migration management, and repeated boilerplate.

It may still be used selectively for performance-sensitive queries in later phases.

### Django ORM

Django ORM is mature, but SentinelAI uses FastAPI and does not require the full Django framework.

### SQLModel

SQLModel integrates Pydantic and SQLAlchemy, but separating API schemas from persistence models provides clearer architectural boundaries for this project.

## Follow-Up Decisions

The following still require confirmation:

* Synchronous or asynchronous SQLAlchemy usage
* Application-generated or database-generated UUIDs
* Session and repository implementation pattern
* Exact testing-database strategy

## Review Condition

Review this decision before:

* Introducing high-volume log ingestion
* Adding analytics-heavy queries
* Introducing multiple database services
* Migrating to a different persistence architecture
