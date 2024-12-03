# Project Management Web Application

## Overview
This is a web-based project management application designed to help teams plan, track, and collaborate on projects efficiently.

## Features
- **Task Management**: Create, update, and manage tasks within a project.
- **subTask Management**: Create, update, and manage subtasks within a task.
- **Progress Tracking**: Visualize task completion and project progress.
- **add-vip users**: users with vip mode have more control and feature than demo users.


## Tech Stack
This project is built with the following technologies:
- **Backend**: djangoDRF
- **Database**: postgresql
- **Authentication**: JWT (JSON Web Tokens) for secure user authentication
- **Secure Passwords**: Passwords are hashed using Argon2, one of the most secure and modern hashing methods.
- **Comprehensive Testing**: All apps, including Tasks, Projects, Financial, and Accounts, are fully tested to ensure functionality and reliability.
- **Admin Panel Enhancements**: Improved admin panel with additional actions and better user control for streamlined management.

## ChangeLog

### [v1.1.0] - 2024-12-02
#### Merge pull request for admin panel
- Updated the admin panel view and added admin actions. (commit: ed376de)
#### Merge pull request for environment configuration
- Added .env configuration and requirements file for environment management. (commit: 55400be)
#### Merge pull request for PostgreSQL support
- Configured the project to use PostgreSQL as the database. (commit: 76efd37)

=====================================================
  
### [v1.0.0] - 2024-11-15
#### Added Financial models
- Developed the financial module and integrated its models and views. (commit: 7b29ea6)
#### Added Projects module
- Introduced the projects module with models, views, and tests. (commit: 395cc5f)
#### Completed Accounts app testing
- Added tests for the Accounts app and resolved related bugs. (commit: 988fa9a)
#### Added Swagger documentation
- Provided Swagger docs for the API endpoints. (commit: 609c504)

=====================================================

### [Initial Development]
#### Added Accounts models
- Introduced user and profile models in the Accounts app. (commit: bff5a4c)
#### Added password hashing and Argon2 integration
- Configured Argon2 for secure password storage. (commit: fde23f4)
#### Initial project setup
- Created the initial project structure and setup. (commit: f4a2fdf)
