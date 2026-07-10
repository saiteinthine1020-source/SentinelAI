# SentinelAI Development Roadmap

## 1. Purpose

This document defines the planned development phases for SentinelAI.

The roadmap is directional and may change through Architecture Decision Records when technical or product requirements evolve.

## Phase 0: Planning and Documentation Foundation

Goal:

Establish the project identity, repository structure, scope, documentation strategy, and GitHub workflow.

Deliverables:

* Repository structure
* README
* Project Overview
* Phase 1 Requirements
* Development Roadmap
* GitHub milestones
* Initial GitHub issues

Completion criteria:

* All planning documents are committed.
* Initial issues and milestones exist.
* The repository is pushed to GitHub.

## Phase 1: Authentication MVP

Goal:

Build the minimum secure user authentication foundation.

Features:

* User registration
* User login
* JWT authentication
* Current-user endpoint
* Protected dashboard
* Logout
* PostgreSQL user table
* Docker Compose environment
* Backend tests

## Phase 2: Log Management MVP

Goal:

Allow authenticated users to upload, store, search, and filter logs.

Features:

* Log upload
* Log validation
* Log storage
* Basic parsing
* Search
* Filtering
* Pagination
* User-owned logs

## Phase 3: Sensitive Data Redaction

Goal:

Protect sensitive information before logs are displayed or sent to AI services.

Features:

* OFF mode
* MASK mode
* DELETE mode
* Email detection
* IP address detection
* Token detection
* AWS key detection
* JWT detection
* Phone number detection
* Custom regular expressions
* Redaction test cases

## Phase 4: AI Log Explanation

Goal:

Provide secure AI-assisted analysis using sanitized logs.

Features:

* AI provider abstraction
* Sanitized log submission
* Log explanation
* Incident summary
* Prompt templates
* Local LLM option
* External AI API option
* Usage safeguards

## Phase 5: Dashboards, Alerts, and Reports

Goal:

Improve visibility and incident response.

Features:

* Event charts
* Severity summaries
* Saved searches
* Alert rules
* Incident reports
* Exportable reports

## Phase 6: Monitoring and Metrics

Goal:

Add system and application observability.

Features:

* Application metrics
* Health checks
* Service monitoring
* Error tracking
* Basic OpenTelemetry support
* Possible Zabbix integration

## Phase 7: AWS Deployment

Goal:

Deploy SentinelAI to AWS using a secure architecture.

Possible services:

* EC2 or ECS
* RDS for PostgreSQL
* Application Load Balancer
* Route 53
* CloudWatch
* S3
* Secrets Manager
* IAM

## Phase 8: CI/CD and Security Hardening

Goal:

Automate quality checks, testing, deployment, and security controls.

Features:

* GitHub Actions
* Automated tests
* Linting
* Dependency scanning
* Container scanning
* Secret scanning
* Security headers
* Backup strategy
* Deployment pipeline

## Phase 9: Enterprise Features

Goal:

Support teams and organizational use cases.

Features:

* RBAC
* Organizations
* Audit logs
* API keys
* Advanced retention policies
* Team dashboards
* Administrative settings

## Phase 10: Product Direction

Goal:

Evaluate SentinelAI as a self-hosted product, SaaS platform, or hybrid solution.

Possible features:

* Multi-tenancy
* Subscription plans
* Tenant isolation
* Usage metering
* Product analytics
* Licensing
* Installation packages
* Customer onboarding

## Roadmap Rule

Only features belonging to the active phase should be implemented.

Advanced features must not be added early unless an approved architectural reason exists.
