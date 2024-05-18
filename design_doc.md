# Design Document

## Overview

This document explains the design choices made for the FastAPI application that supports creating, getting, and updating leads. The application includes a publicly available form for prospects to fill out, an internal UI guarded by authentication to manage leads, and email notifications.

## Functional Requirements

- **Create Lead:** Collects first name, last name, email, and resume/CV from prospects.
- **Get Leads:** Retrieves a list of all leads.
- **Update Lead State:** Allows an internal user to update the state of a lead from `PENDING` to `REACHED_OUT`.
- **Email Notifications:** Sends an email to the prospect and an internal attorney upon lead submission.

## Tech Stack

- **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.6+.
- **SQLite:** A lightweight, disk-based database that doesn’t require a separate server process.
- **SQLAlchemy:** SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **SMTP:** Simple Mail Transfer Protocol for sending emails.

## Design Choices

### 1. SQLite

**Why SQLite?**
- **Simplicity:** SQLite is easy to set up and doesn't require a separate server process, making it ideal for lightweight applications and prototyping.
- **Local Development:** Ideal for development and testing environments. For production, you can switch to a more robust database like PostgreSQL or MySQL.

### 2. SQLAlchemy

**Why SQLAlchemy?**
- **ORM Capabilities:** SQLAlchemy provides a high-level ORM that allows for easy database interactions using Python objects.
- **Flexibility:** SQLAlchemy supports both ORM and SQL expression language, offering flexibility in how we interact with the database.

### 3. OAuth2 for Authentication

**Why OAuth2?**
- **Security:** OAuth2 is a robust and widely-used protocol for securing APIs.
- **Integration:** FastAPI's support for OAuth2 makes it straightforward to implement secure authentication mechanisms.

### 4. SMTP for Email Notifications

**Why SMTP?**
- **Simplicity:** Using SMTP is straightforward for sending emails from the application.
- **Compatibility:** SMTP is widely supported and can be easily configured to use different email providers.

## Application Structure

### Main Application Code (`api.py`)

The main application code includes the FastAPI instance, models, schemas, and route handlers. The structure ensures that the application is easy to understand and maintain.

### Environment Variables

Sensitive information like email credentials is stored in environment variables to enhance security. This prevents hardcoding sensitive data in the source code.

### Error Handling

The application includes error handling to manage exceptions that may occur during database operations or email sending. This ensures that the application can handle failures gracefully and provide meaningful error messages to the client.

### Email Sending

Two utility functions are provided for sending emails to the prospect and the attorney. These functions use the `smtplib` module to send emails via an SMTP server. Environment variables are used to store email credentials securely.

## Future Improvements

- **Production-Ready Database:** Switch to a more robust database like PostgreSQL or MySQL for production environments.
- **Email Sending Service:** Use a dedicated email sending service (like SendGrid or AWS SES) for better reliability and security.
- **Detailed Logging:** Implement detailed logging to help with debugging and monitoring.
- **Detailed API Responses** Instead of returning the concrete field that's missing in case of a bad request I would just return a 400 Error and a generic "Bad Request" response
- **Environment Variables** Passwords and emails should be stored in env variables 
- **Structuring the Code** As Readme.md shows, the code should be more structured. A posibility could be: 

```angular2html
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
└── utils
    └── email.py
```

## Conclusion

The design choices made for this application aim to balance simplicity, performance, and security. With FastAPI, SQLAlchemy, and SQLite, I have created a lightweight, maintainable, and high-performing application that meets the specified functional requirements.
