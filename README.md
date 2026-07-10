# SentinelAI

SentinelAI is a long-term portfolio and product-style project for building an AI-powered security and observability web application.

The project is inspired by platforms and tools such as Splunk, Grafana, ChatGPT, Claude, and local LLM systems.

## Project Vision

SentinelAI aims to help engineers, security teams, and small organizations collect, search, analyze, and understand system and security logs.

The long-term product vision includes:

* Log collection and ingestion
* Log search and filtering
* Security event visualization
* Sensitive data redaction
* AI-powered log explanation
* Incident summaries
* Reports
* Alerts
* System monitoring
* Self-hosted deployment
* Optional SaaS deployment

## Current Project Phase

```text
Phase 0: Planning and documentation foundation
```

The next phase is:

```text
Phase 1: Authentication MVP
```

## Phase 1 Scope

Phase 1 includes:

* User registration
* User login
* JWT authentication
* Dashboard page
* Logout
* PostgreSQL user table
* Docker Compose development environment
* Backend tests
* Basic project documentation

Phase 1 does not include:

* AI integration
* Log upload
* Log search
* Sensitive data redaction
* Alerts
* Monitoring
* AWS deployment
* Kubernetes
* RBAC
* Enterprise features

## Technology Stack

### Frontend

* React
* TypeScript
* Tailwind CSS

### Backend

* Python
* FastAPI

### Database

* PostgreSQL

### Authentication

* JWT

### Development Environment

* Docker
* Docker Compose

### Testing

* Pytest
* Frontend testing will be added later

### Cloud

* AWS will be introduced in a later phase

### AI

* Google AI Studio API or a local LLM will be introduced in a later phase

## Repository Structure

```text
SentinelAI/
├── frontend/
├── backend/
├── database/
├── docs/
│   ├── en/
│   ├── ja/
│   └── templates/
├── scripts/
├── infrastructure/
├── docker/
├── assets/
├── .github/
├── docker-compose.yml
├── README.md
├── README_ja.md
├── .gitignore
└── LICENSE
```

## Documentation

English documentation is the primary source of truth.

Japanese documentation will also be maintained to demonstrate documentation practices used in Japanese IT companies.

Main documentation includes:

* Project Overview
* Requirements Definition
* Development Roadmap
* Basic Design
* Database Design
* API Design
* Screen Design
* Setup Guide
* Test Specification
* Operation Manual
* Release Notes
* Architecture Decision Records

## Development Principles

SentinelAI is developed incrementally like a real product.

The project prioritizes:

* Security
* Maintainability
* Clean architecture
* Clear documentation
* Testability
* Professional Git practices
* Realistic production-style development

Engineering quality is more important than development speed.

## Project Status

SentinelAI is currently in the planning and documentation foundation phase.

Application development has not started yet.
