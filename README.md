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

### [1.0.0] - 2024-12-01
#### Added
- Initial release with basic task management features.
- User authentication using JWT.
- Ability to create and manage users.

### [1.0.1] - 2024-12-01
#### Fixed
- Fix problme with logout wich user could access endpoints after logout.

### [1.0.2] - 2024-12-01
#### Added
- add vip user mode to app

### [1.2.0] - 2024-12-01
#### Added
- add project model
- basic managements on projects
