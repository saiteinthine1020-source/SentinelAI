# SentinelAI Project Overview

## 1. Project Name

SentinelAI

## 2. Project Concept# SentinelAI Project Overview

## 1. Document Information

| Item             | Value            |
| ---------------- | ---------------- |
| Project Name     | SentinelAI       |
| Document         | Project Overview |
| Status           | Draft            |
| Current Phase    | Phase 0          |
| Primary Language | English          |
| Last Updated     | 2026-07-10       |

## 2. Project Purpose

SentinelAI is a security and observability web application designed to help users collect, search, analyze, and understand system and security logs.

The project is also intended to demonstrate professional engineering capabilities across full-stack development, cybersecurity, cloud engineering, networking, DevOps, observability, AI integration, testing, and technical documentation.

## 3. Problem Statement

System and security logs are often difficult to understand, especially for junior engineers and small teams.

Existing enterprise platforms can be powerful but may also be expensive, complex, or difficult to configure.

Logs may also contain sensitive data such as:

* Email addresses
* Passwords
* API keys
* Access tokens
* JWT tokens
* AWS credentials
* IP addresses
* Internal hostnames
* Phone numbers
* Payment-related values

Sending raw logs directly to an external AI service may create security and privacy risks.

SentinelAI aims to address these problems through structured log management, sensitive data redaction, secure AI processing, and clear incident explanations.

## 4. Product Vision

The long-term vision is to build SentinelAI as a self-hosted security and observability platform with an optional SaaS direction.

The platform should eventually allow users to:

* Collect and upload logs
* Search and filter logs
* Visualize system and security events
* Detect suspicious activity
* Redact sensitive values
* Ask AI to explain logs
* Generate incident summaries
* Create reports
* Configure alerts
* Monitor service health

## 5. Target Users

Initial target users:

* Junior system engineers
* Junior security engineers
* DevOps learners
* Small engineering teams
* Developers who need a simple log analysis tool

Future target users:

* Small and medium-sized companies
* Security operations teams
* DevOps teams
* Managed service providers
* Self-hosted software users

## 6. Project Goals

The project goals are:

1. Build a maintainable full-stack application.
2. Apply secure authentication and data handling.
3. Demonstrate professional API and database design.
4. Use Docker for reproducible local development.
5. Implement testing and documentation from the beginning.
6. Add observability and AI features gradually.
7. Prepare the system for future AWS deployment.
8. Create a portfolio project that demonstrates realistic engineering skills.

## 7. Non-Goals

SentinelAI is not intended to:

* Replace Splunk in the early phases
* Support enterprise-scale log ingestion initially
* Provide real-time SOC automation in Phase 1
* Include advanced machine learning in the MVP
* Support Kubernetes at the beginning
* Become a complete SaaS platform immediately

## 8. High-Level Product Flow

Future product flow:

```text
Log Source
    ↓
Log Collection or Upload
    ↓
Validation and Parsing
    ↓
Sensitive Data Detection
    ↓
Mask or Delete Sensitive Data
    ↓
Secure Storage
    ↓
Search and Visualization
    ↓
Optional AI Analysis
    ↓
Incident Explanation or Report
```

## 9. Development Approach

The project will be developed in phases.

Each phase will include:

* Defined scope
* Design documents
* Implementation
* Tests
* Documentation updates
* GitHub issues
* Review criteria
* Release notes

## 10. Success Criteria

Phase 0 is complete when:

* The repository structure exists.
* The README files are complete.
* The project overview is complete.
* Phase 1 requirements are documented.
* The development roadmap is documented.
* GitHub milestones and initial issues exist.
* All Day 0 work is pushed to GitHub.


SentinelAI is an AI-powered security and observability web application designed to help users collect, search, analyze, and understand system and security logs.

The long-term goal is to build a production-style platform inspired by Splunk, Grafana, ChatGPT, Claude, and local LLM-based tools.

## 3. Project Purpose

This project is built as a long-term portfolio and product-style engineering project to demonstrate:

* Full-stack web development
* Backend API design
* Authentication and security
* PostgreSQL database design
* Docker-based development
* Observability and log handling
* AI integration
* Secure handling of sensitive log data
* Professional documentation

## 4. Product Vision

SentinelAI should eventually help users and companies:

* Upload and store logs
* Search and filter logs
* Visualize security and system events
* Detect suspicious activity
* Redact sensitive data before AI analysis
* Ask AI to explain logs and summarize incidents
* Generate incident reports
* Monitor system health
* Receive alerts

## 5. Long-Term Security Concept

Because logs may contain sensitive information, SentinelAI will eventually include a Sensitive Data Redaction Layer.

Example flow:

Raw Log
↓
Sensitive Data Detection
↓
Mask or Delete Sensitive Values
↓
Sanitized Log
↓
AI Analysis
↓
Report or Explanation

## 6. Phase 1 Scope

Phase 1 focuses only on the authentication MVP.

Included:

* User registration
* User login
* JWT authentication
* Dashboard page
* Logout
* PostgreSQL user table
* Docker Compose development environment
* Basic README
* Basic documentation

Not included in Phase 1:

* AI analysis
* Log upload
* Log search
* Redaction
* Alerts
* Monitoring
* AWS deployment
* Kubernetes
* RBAC
* SaaS features

## 7. Target Users

Initial target users:

* Engineers who want to inspect system or security logs
* Junior security engineers learning log analysis
* Small teams that need a simple self-hosted observability tool

Future target users:

* Small and medium-sized companies
* Security teams
* DevOps teams
* Managed service providers

## 8. Main Tech Stack

Frontend:

* React
* TypeScript
* Tailwind CSS

Backend:

* Python
* FastAPI

Database:

* PostgreSQL

Authentication:

* JWT

Infrastructure:

* Docker
* Docker Compose

Version Control:

* Git
* GitHub

Testing:

* Pytest for backend
* Frontend tests in later phases

## 9. Development Policy

SentinelAI will be developed step by step.

The project will prioritize:

* Security
* Clean architecture
* Maintainability
* Documentation quality
* Realistic production-style design
* Professional GitHub workflow

Speed is not the priority. Engineering quality is the priority.
