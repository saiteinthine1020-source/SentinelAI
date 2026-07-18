# SentinelAI Phase 1 Screen Design

## 1. Document Information

| Item             | Value                        |
| ---------------- | ---------------------------- |
| Project          | SentinelAI                   |
| Document         | Phase 1 Screen Design        |
| Phase            | Phase 1 — Authentication MVP |
| Status           | Draft                        |
| Frontend         | React + TypeScript           |
| Styling          | Tailwind CSS                 |
| Primary Language | English                      |
| Last Updated     | 2026-07-12                   |

## 2. Purpose

This document defines the frontend screens, navigation behavior, validation states, loading states, error states, and authentication-related user experience for the SentinelAI Phase 1 Authentication MVP.

The screen design covers:

* Registration page
* Login page
* Protected dashboard page
* Authentication-loading state
* Unauthorized state
* Logout behavior
* Basic responsive behavior

This document does not include log management, AI analysis, alerts, monitoring, administration, or enterprise screens.

## 3. Design Principles

The Phase 1 frontend should follow these principles:

* Keep the interface simple and focused.
* Prioritize clarity over visual complexity.
* Provide immediate validation feedback.
* Avoid exposing technical implementation details to users.
* Do not display passwords, JWT values, or internal errors.
* Make authentication state clear.
* Support desktop and mobile layouts.
* Use accessible labels and form controls.
* Use consistent spacing, typography, and button behavior.
* Keep the visual style suitable for a security and observability product.

## 4. Phase 1 Route Map

| Route        | Screen            | Authentication | Purpose                        |
| ------------ | ----------------- | -------------- | ------------------------------ |
| `/register`  | Registration Page | Public         | Create a user account          |
| `/login`     | Login Page        | Public         | Authenticate a registered user |
| `/dashboard` | Dashboard Page    | Required       | Show authenticated user access |
| `*`          | Not Found State   | Public         | Handle unknown routes          |

## 5. Navigation Rules

### 5.1 Public User

A user without a valid session may access:

* `/register`
* `/login`

A public user who attempts to access `/dashboard` must be redirected to:

```text
/login
```

### 5.2 Authenticated User

An authenticated user may access:

* `/dashboard`

If an authenticated user opens `/login` or `/register`, the frontend should redirect the user to:

```text
/dashboard
```

This avoids displaying authentication forms to an already authenticated user.

### 5.3 Unknown Route

An unknown route should display a simple Not Found state.

Recommended actions:

* Return to login if unauthenticated
* Return to dashboard if authenticated

## 6. Shared Application Layout

Phase 1 uses two layout types:

### 6.1 Authentication Layout

Used by:

* Registration page
* Login page

Structure:

```text
┌────────────────────────────────────────────┐
│ SentinelAI logo or wordmark                │
│                                            │
│ ┌────────────────────────────────────────┐ │
│ │ Authentication card                    │ │
│ │                                        │ │
│ │ Page title                             │ │
│ │ Supporting text                        │ │
│ │ Form fields                            │ │
│ │ Primary action                         │ │
│ │ Navigation link                        │ │
│ └────────────────────────────────────────┘ │
│                                            │
│ Optional minimal footer                    │
└────────────────────────────────────────────┘
```

### 6.2 Application Layout

Used by:

* Dashboard page

Structure:

```text
┌────────────────────────────────────────────┐
│ Header                                     │
│ SentinelAI           User        Logout    │
├────────────────────────────────────────────┤
│ Main content                               │
│                                            │
│ Welcome card                               │
│ Account information                        │
│ Phase 1 status                             │
│                                            │
└────────────────────────────────────────────┘
```

## 7. Visual Direction

The Phase 1 interface should communicate:

* Security
* Reliability
* Modern engineering
* Clear system status
* Minimal complexity

Recommended visual characteristics:

* Dark or neutral background
* High-contrast readable text
* Card-based authentication forms
* Clear primary action buttons
* Subtle borders
* Limited accent color
* Consistent corner radius
* Minimal animation

Avoid:

* Excessive gradients
* Decorative animation
* Dense dashboards
* Fake security metrics
* Log charts before Phase 2
* AI chat elements before Phase 4

## 8. Registration Page

### 8.1 Route

```text
/register
```

### 8.2 Purpose

Allow a new user to create a SentinelAI account.

### 8.3 Page Structure

```text
SentinelAI

Create your account

Start building your secure observability workspace.

Username
[____________________________]

Email address
[____________________________]

Password
[____________________________]

Confirm password
[____________________________]

[ Create account ]

Already have an account? Sign in
```

### 8.4 Form Fields

| Field            | Type     | Required | Browser Autocomplete | Notes                      |
| ---------------- | -------- | -------: | -------------------- | -------------------------- |
| Username         | Text     |      Yes | `username`           | 3–50 permitted characters  |
| Email            | Email    |      Yes | `email`              | Normalized by backend      |
| Password         | Password |      Yes | `new-password`       | 12–128 characters          |
| Confirm Password | Password |      Yes | `new-password`       | Frontend-only confirmation |

### 8.5 Username Validation

Frontend validation:

* Required
* Minimum 3 characters
* Maximum 50 characters
* Allowed pattern:

```text
^[A-Za-z0-9_-]{3,50}$
```

Suggested user message:

```text
Use 3–50 letters, numbers, underscores, or hyphens.
```

### 8.6 Email Validation

Frontend validation:

* Required
* Valid email-like format
* Maximum 254 characters
* Leading and trailing whitespace removed before submission

Suggested messages:

```text
Email address is required.
```

```text
Enter a valid email address.
```

### 8.7 Password Validation

Frontend rules:

* Minimum 12 characters
* Maximum 128 characters
* At least one uppercase letter
* At least one lowercase letter
* At least one number
* At least one special character

Display a compact password requirement list.

Example:

```text
Password requirements:
✓ At least 12 characters
✓ Uppercase letter
✓ Lowercase letter
✓ Number
✓ Special character
```

Requirements may update visually while the user types.

The backend remains authoritative.

### 8.8 Confirm Password Validation

Rules:

* Required
* Must match the password field

Suggested error:

```text
Passwords do not match.
```

### 8.9 Submit Button States

Default:

```text
Create account
```

Loading:

```text
Creating account...
```

Disabled when:

* Request is in progress
* Required fields are empty
* Frontend validation fails

The button must prevent duplicate submissions.

### 8.10 Registration Success

After a successful `201 Created` response:

1. Show a brief success message.
2. Redirect to `/login`.
3. Optionally prefill the normalized email address.

Suggested message:

```text
Account created successfully. Sign in to continue.
```

Registration must not automatically authenticate the user in Phase 1.

### 8.11 Registration Errors

#### Duplicate Email

```text
An account with this email already exists.
```

#### Duplicate Username

```text
This username is already in use.
```

#### Password Policy Failure

```text
Your password does not meet the security requirements.
```

#### Validation Failure

Display field-specific messages where possible.

#### Unexpected Failure

```text
We could not create your account. Please try again.
```

Do not display backend stack traces or database messages.

## 9. Login Page

### 9.1 Route

```text
/login
```

### 9.2 Purpose

Allow a registered user to authenticate and access the dashboard.

### 9.3 Page Structure

```text
SentinelAI

Welcome back

Sign in to access your workspace.

Email address
[____________________________]

Password
[____________________________]

[ Sign in ]

Do not have an account? Create one
```

### 9.4 Form Fields

| Field    | Type     | Required | Browser Autocomplete |
| -------- | -------- | -------: | -------------------- |
| Email    | Email    |      Yes | `email`              |
| Password | Password |      Yes | `current-password`   |

### 9.5 Validation

Email:

* Required
* Valid email-like format

Password:

* Required

The login form should not repeat the full registration password-policy checklist.

### 9.6 Submit Button States

Default:

```text
Sign in
```

Loading:

```text
Signing in...
```

Disabled while:

* Request is in progress
* Required fields are missing
* Frontend validation fails

### 9.7 Login Success

After a successful login:

1. The backend sets the HttpOnly cookie.
2. The frontend requests `/api/v1/auth/me`.
3. The frontend stores safe user information in memory.
4. The frontend redirects to `/dashboard`.

The frontend must not attempt to read the JWT.

### 9.8 Login Errors

#### Invalid Credentials

```text
Invalid email or password.
```

Use the same message for unknown email and incorrect password.

#### Inactive Account

```text
Your account is currently disabled.
```

#### Validation Failure

Display a relevant field message.

#### Unexpected Failure

```text
We could not sign you in. Please try again.
```

## 10. Dashboard Page

### 10.1 Route

```text
/dashboard
```

### 10.2 Authentication

Required.

The page must not render authenticated content until the frontend confirms the session using:

```text
GET /api/v1/auth/me
```

### 10.3 Purpose

Provide a simple protected landing page confirming that authentication works.

The dashboard is intentionally minimal during Phase 1.

### 10.4 Page Structure

```text
┌────────────────────────────────────────────┐
│ SentinelAI                    Sai  Logout   │
├────────────────────────────────────────────┤
│                                            │
│ Welcome to SentinelAI                      │
│                                            │
│ Authentication is working successfully.    │
│                                            │
│ Account                                    │
│ Username: sai                              │
│ Email: sai@example.com                     │
│ Status: Active                             │
│                                            │
│ Phase 1                                    │
│ Authentication MVP                         │
│                                            │
└────────────────────────────────────────────┘
```

### 10.5 Displayed User Data

The dashboard may display:

* Username
* Email
* Active status
* Account creation date

The dashboard must not display:

* Password
* Password hash
* JWT
* Cookie value
* Database identifier unless intentionally required
* Internal security configuration

### 10.6 Dashboard Content

Suggested sections:

#### Welcome Card

```text
Welcome to SentinelAI
```

```text
Your authentication session is active.
```

#### Account Card

Displays safe user information.

#### Project Phase Card

Displays:

```text
Current phase: Phase 1 — Authentication MVP
```

Do not add fake logs, charts, alerts, or AI output.

## 11. Authentication Loading State

When the application starts or a protected page is opened, the authentication status may be unknown.

During this period, display a loading state.

Example:

```text
Checking your session...
```

Recommended behavior:

* Do not briefly show the login page before the session check finishes.
* Do not briefly show protected dashboard content before authentication is confirmed.
* Avoid route flickering.

Possible state model:

```text
loading
authenticated
unauthenticated
error
```

## 12. Unauthorized State

When `/api/v1/auth/me` returns `401`:

1. Clear safe frontend user state.
2. Redirect to `/login`.
3. Optionally preserve the intended destination for future enhancement.

Suggested message:

```text
Your session has expired. Please sign in again.
```

Do not repeatedly call the endpoint in a redirect loop.

## 13. Inactive Account State

When the backend returns `403` for an inactive account:

1. Clear frontend authentication state.
2. Redirect to `/login`.
3. Display:

```text
Your account is currently disabled.
```

The frontend must not treat an inactive user as authenticated.

## 14. Logout Design

### 14.1 Logout Control

The dashboard header should contain a visible logout control.

Recommended label:

```text
Logout
```

### 14.2 Logout Flow

When selected:

1. Disable the logout control temporarily.
2. Send:

```text
POST /api/v1/auth/logout
```

3. Include credentials.
4. Clear safe frontend user state.
5. Redirect to `/login`.

### 14.3 Logout Loading State

Optional text:

```text
Signing out...
```

### 14.4 Logout Failure

Even if the network request fails, the frontend should clear local non-sensitive authentication state and redirect to login.

The backend cookie may remain until expiration if the logout request did not reach the server.

Suggested generic message on the login page:

```text
You have been signed out locally.
```

## 15. Not Found State

Unknown routes should display:

```text
Page not found
```

Suggested action:

```text
Return to SentinelAI
```

Redirect destination:

* `/dashboard` for an authenticated user
* `/login` for an unauthenticated user

## 16. Form Error Presentation

Errors should be displayed near the affected field when possible.

Example:

```text
Email address
[invalid@example]
Enter a valid email address.
```

General form errors should appear above the primary button.

Example:

```text
Invalid email or password.
```

Error styling should:

* Be visible
* Use readable contrast
* Include text, not color alone
* Avoid exposing technical details

## 17. Accessibility Requirements

Phase 1 screens should include:

* Visible form labels
* Keyboard-accessible controls
* Logical tab order
* Button text that describes the action
* Error messages connected to fields
* Visible focus indicators
* Sufficient text contrast
* Semantic headings
* Appropriate input types
* Screen-reader-compatible status messages

Do not use placeholders as the only form labels.

## 18. Responsive Design

### Desktop

* Centered authentication card
* Maximum readable form width
* Spacious layout
* Header with user and logout controls

### Tablet

* Reduced side margins
* Full-width cards within a constrained container

### Mobile

* Single-column layout
* Full-width form controls
* Touch-friendly buttons
* Compact header
* No horizontal scrolling

Recommended minimum supported width:

```text
320px
```

## 19. Frontend State Design

Recommended authentication state:

```typescript
type AuthState =
  | { status: "loading"; user: null }
  | { status: "authenticated"; user: PublicUser }
  | { status: "unauthenticated"; user: null }
  | { status: "error"; user: null };
```

The state stores only safe public user information.

The state must not store:

* JWT
* Password
* Password hash
* Cookie value

## 20. API Client Requirements

The frontend API client must:

* Use the configured API base URL
* Send credentials with authentication requests
* Parse JSON responses
* Handle `401` consistently
* Handle `403` consistently
* Avoid logging sensitive request data
* Avoid duplicating API configuration in every component

Recommended centralized client configuration:

```text
Base URL: VITE_API_BASE_URL
Credentials: enabled
Content type: application/json
```

## 21. Planned Frontend Structure

Conceptual structure:

```text
frontend/src/
├── app/
│   ├── router/
│   └── providers/
├── components/
│   ├── ui/
│   └── layout/
├── features/
│   └── auth/
│       ├── api/
│       ├── components/
│       ├── hooks/
│       ├── schemas/
│       └── types/
├── pages/
│   ├── LoginPage.tsx
│   ├── RegisterPage.tsx
│   ├── DashboardPage.tsx
│   └── NotFoundPage.tsx
├── lib/
│   └── api-client.ts
└── main.tsx
```

This is a planned structure and may be refined before implementation.

## 22. Frontend Testing Requirements

### Registration Page

* Required field validation
* Invalid username
* Invalid email
* Weak password
* Password mismatch
* Loading state
* Successful registration redirect
* Duplicate email error
* Duplicate username error

### Login Page

* Required field validation
* Invalid email
* Loading state
* Successful login redirect
* Invalid credential error
* Inactive account error

### Dashboard

* Loading state
* Authenticated user display
* Unauthenticated redirect
* Expired-session redirect
* Logout behavior

### Accessibility

* Inputs have labels
* Form errors are discoverable
* Buttons are keyboard accessible
* Focus behavior is reasonable

Frontend tests may be introduced after the backend authentication MVP is stable.

## 23. Open Screen Decisions

| ID     | Decision                                                            | Status   |
| ------ | ------------------------------------------------------------------- | -------- |
| UI-001 | Authentication pages use a centered card layout                     | Accepted |
| UI-002 | Dashboard remains minimal in Phase 1                                | Accepted |
| UI-003 | Safe user state is stored in memory only                            | Accepted |
| UI-004 | JWT is never stored in frontend state                               | Accepted |
| UI-005 | Authenticated users are redirected away from login and registration | Accepted |
| UI-006 | Form library: React Hook Form                                       | Accepted |
| UI-007 | Frontend validation library: Zod                                    | Accepted |
| UI-008 | API client: Axios                                                   | Accepted |
| UI-009 | Final color palette and branding                                    | Deferred |
| UI-010 | Detailed design system                                              | Deferred |

## 24. Screen Design Completion Criteria

The Phase 1 frontend implementation is complete when:

* Registration page matches this design.
* Login page matches this design.
* Dashboard is protected.
* Authentication loading state is implemented.
* Unauthorized users are redirected.
* Inactive accounts are handled.
* Logout is implemented.
* Forms provide clear validation.
* Credentialed API requests are configured.
* Sensitive authentication data is not stored in frontend state.
* Responsive behavior works at supported widths.
* Accessibility basics are implemented.
* Screen behavior matches the API and authentication documents.

## Implementation Status

Implemented:

* React and TypeScript application
* Vite development environment
* Tailwind CSS integration
* React Router configuration
* Centralized Axios client
* React Hook Form dependency
* Zod validation schemas
* Authentication feature folders
* Login placeholder page
* Dashboard placeholder page
* Not Found page
* Shared authentication and application layouts
* Registration form
* Frontend registration validation
* Loading state
* Backend conflict error display
* Successful registration redirect
* Login-page registration success message

Not yet implemented:

* Login form submission
* Authentication provider
* Protected routes
* Current-user session loading
* Logout behavior
