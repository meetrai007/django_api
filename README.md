# ToDo Project with Django REST Framework (DRF)

## Introduction
This is a simple and functional ToDo application built using Django REST Framework (DRF) and Ninja API. The project provides RESTful APIs for managing to-do tasks and user authentication using JWT tokens. Swagger UI is integrated for API documentation.

## Features
- **User Authentication**: Secure user authentication using JWT tokens.
- **CRUD Operations**: Create, read, update, and delete to-do tasks.
- **API Documentation**: Interactive API documentation using Swagger.
- **Ninja API Integration**: Example router-based endpoints.

## Technologies Used
- Python
- Django
- Django REST Framework (DRF)
- Ninja API
- Swagger (drf_yasg)
- JWT Authentication

## Project Structure
```
todo_project/
    |-- manage.py
    |-- todos/
        |-- views.py
        |-- models.py
        |-- serializers.py
        |-- urls.py
        |-- schema.py
```

## API Endpoints
### User Management
- **Create User**: `/create-user/`
- **Login User**: `/login-user/`
- **JWT Token**: `/api/token/`
- **Refresh Token**: `/api/token/refresh/`

### Todo Management
- **List/Create Todos**: `/todos/`
- **Retrieve/Update/Delete Todo**: `/todos/<id>/`

### Ninja API
- **User List**: `/api/users/list/`
- **Create User Example**: `/api/users/create/`

### API Documentation
- **Swagger UI**: `/swagger/`

## Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd todo_project
```

### Step 2: Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate    # For Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Start the Development Server
```bash
python manage.py runserver
```

### Step 6: Access the Application
- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

## Usage
1. Create a user using the `/create-user/` endpoint.
2. Obtain JWT tokens via the `/api/token/` endpoint.
3. Use the token in the `Authorization` header as `Bearer <your_token>`.
4. Manage to-do tasks using the `/todos/` endpoints.

## Example JWT Authentication Request
### Request
```bash
POST /api/token/
```
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```

### Response
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

## Contributing
Feel free to fork the repository and contribute by submitting a pull request.

## License
This project is licensed under the MIT License.

## Contact
For more information or queries, please contact [your email or GitHub link].

---

Thank you for checking out this simple ToDo project using Django REST Framework!

