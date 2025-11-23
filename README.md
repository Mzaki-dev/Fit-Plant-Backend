# Fit Plant Backend

A FastAPI backend with user roles (admin and worker). Admins can perform CRUD operations on workers and tasks.

## Project Structure

```
fit_plant_backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       └── tasks.py
├── tests/
├── requirements.txt
├── README.md
├── main.py (entry point)
└── create_admin.py
```

## Setup

1. Install dependencies: `pip install -r requirements.txt`

2. Create initial admin: `python create_admin.py`

3. Run the server: `uvicorn main:app --reload`

## API Endpoints

- `POST /token`: Sign-in to get access token (JWT-based authentication)
- `GET /users/me/`: Get current user info
- `GET /api/workers/`: Get list of workers (admin only)
- `POST /api/workers/`: Create a new worker (admin only) - requires password and confirm_password, optional profile_image upload
- `PUT /api/workers/{user_id}`: Update a worker (admin only)
- `DELETE /api/workers/{user_id}`: Delete a worker (admin only)
- `GET /api/tasks/`: Get list of tasks (admin only)
- `POST /api/tasks/`: Create a new task (admin only)
- `PUT /api/tasks/{task_id}`: Update a task (admin only)
- `DELETE /api/tasks/{task_id}`: Delete a task (admin only)

## Authentication

Uses JWT tokens for role-based access control. Admins have full access to worker management, while workers can only access their own info.

## Environment Variables

Create a `.env` file in the root directory:

```
DATABASE_URL=postgresql://your_username:your_password@localhost/fitplant
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Update `alembic.ini` with the same DATABASE_URL for migrations.

## Running Migrations

- Generate new migration: `alembic revision --autogenerate -m "message"`
- Apply migrations: `alembic upgrade head`
- Rollback: `alembic downgrade -1`

## Security

Change the SECRET_KEY in `app/auth/auth.py` for production.