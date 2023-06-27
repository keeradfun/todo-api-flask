# Flask Todo App API with JWT-based User Authentication

## About

This repository contains a Flask-based Todo App API that incorporates user authentication using JSON Web Tokens (JWT). The API allows users to create tasks and ensures that each task can only be accessed by the user who created it.

## Features

- **User registration and login**: Users can create an account and authenticate themselves using JWT.
- **User Hierarchy**: Super Admin and Normal User roles exist.
- **User Active Status**: Super Admin has the ability to toggle user status (active/inactive).
- **JWT-based authentication**: JSON Web Tokens are used to secure API endpoints and authenticate user requests.
- **Task management**: Users can create, retrieve, update, and delete their tasks.
- **Task ownership**: Each task is associated with the user who created it, ensuring that only the respective user can access and modify the task.
- **RESTful API**: The API follows the principles of a RESTful architecture for easy integration and scalability.
- **Data persistence**: Tasks and user information are stored in a database to maintain data integrity.

## Techstack

- **Python 3.11.2**: The programming language used for the project.
- **Flask RestFul**: A lightweight and flexible web framework for building RESTful APIs in Python.
- **PostgreSQL**: A powerful open-source relational database management system.
- **SQLAlchemy**: A powerful and popular Object-Relational Mapping (ORM) library for Python, used for interacting with databases.
- **Marshmallow**: A Python library used for object serialization/deserialization, including validation, and transforming complex data types to and from Python objects.
- **Flask JWT Extended**: An extension for Flask that provides JSON Web Token (JWT) authentication support, allowing secure user authentication and authorization in the API.
- **Bcrypt**: A password-hashing function/library used for secure password storage and authentication.

## Getting Started

1. Clone Repository
   `https://github.com/keeradfun/todo-api-flask.git`
2. Create virtual environment and activate
   - Linux :

```
python -m venv env
source env/bin/activate
```

- Windows :

```
python -m venv env
env\Script\activate.bat
```

3. Go to project root and install all the requirements from requirements.txt
   ```
   cd todo-api-flask
   python -m pip install -r requirements.txt
   ```
4. rename/copy sample-env as .env and edit it with appropriate settings
5. execute - flask --app app --debug run to run as development mode

## Windows

```
install python
python -m pip install virtualenv
python -m venv env
env/Scripts/activate.bat #to activate virtual env
flask --app app --debug run
```
