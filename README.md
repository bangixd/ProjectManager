# Project Management Web Application

## Overview
This is a web-based project management application designed to help teams plan, track, and collaborate on projects efficiently. The app provides features for task management, progress tracking, team collaboration, and reporting. The goal of this project is to simplify project management and improve team coordination through a user-friendly interface and real-time updates.

## Features
- **Task Management**: Create, update, and manage tasks within a project.
- **subTask Management**: Create, update, and manage subtasks within a task.
- **Progress Tracking**: Visualize task completion and project progress.
- **add-vip users**: users with vip mode have more control and feature than demo users.
- **Custom Reporting**: Generate reports on project progress, completed tasks, and resource usage. (under development)


## Tech Stack
This project is built with the following technologies:
- **Backend**: djangoDRF
- **Database**: postgresql
- **Authentication**: JWT (JSON Web Tokens) for secure user authentication

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
