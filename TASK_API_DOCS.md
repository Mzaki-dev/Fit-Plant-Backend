# Task Management API Documentation

## Overview
Complete backend implementation for task management in Fit Plant Backend.
Admins can create, view, edit, and delete tasks assigned to workers.

## Database Schema
Tasks table includes:
- id (Primary Key)
- title (String)
- description (String)
- crop_type (String)
- due_date (DateTime)
- assigned_to (Foreign Key to users.id, must be worker)
- status (Enum: pending, in_progress, completed)
- created_by (Foreign Key to users.id, admin)
- created_at (DateTime)
- updated_at (DateTime)
- image_path (String, nullable) - Path to uploaded image when task is completed
- plant_condition (String, nullable) - Description of plant condition provided by worker

## API Endpoints

### 1. Create Task
**POST** `/api/tasks/`
**Auth**: Admin JWT required
**Body**:
```json
{
  "title": "Task Title",
  "description": "Task Description",
  "crop_type": "Wheat",
  "due_date": "2025-12-01T00:00:00",
  "assigned_to": 2,
  "severity": "medium"
}
```
**Response**: Created task object
**Validation**: assigned_to must be a user with role="worker"

### 2. Get All Tasks
**GET** `/api/tasks/`
**Auth**: JWT required (admin sees all tasks, worker sees only their assigned tasks)
**Query Params**: page=1, limit=10, search, status, worker_id
**Response**: Paginated tasks with metadata
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task 1: Planting Wheat",
      "description": "Plant wheat in field 5",
      "crop_type": "Wheat",
      "due_date": "2025-12-01T00:00:00",
      "assigned_to": 2,
      "status": "pending",
      "severity": "medium",
      "created_by": 1,
      "created_at": "2025-11-23T10:00:00",
      "updated_at": "2025-11-23T10:00:00",
      "worker_name": "John Doe",
      "image_path": null,
      "plant_condition": null
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "total_pages": 1
}
```

### 2.1 Get Single Task
**GET** `/api/tasks/{task_id}`
**Auth**: JWT required
**Permissions**: 
- Admin: Can view any task
- Worker: Can only view tasks assigned to them
**Response**: Single task object with worker_name, image_path, plant_condition

### 3. Update Task
**PUT** `/api/tasks/{task_id}`
**Auth**: Admin JWT required
**Body**: Partial update (any combination of create fields including severity)
**Response**: Updated task object

### 4. Delete Task
**DELETE** `/api/tasks/{task_id}`
**Auth**: Admin JWT required
**Response**: `{"message": "Task deleted"}`

### 5. Complete Task (Worker)
**PUT** `/api/tasks/{task_id}/complete`
**Auth**: Worker JWT required
**Content-Type**: multipart/form-data
**Body**:
- `plant_condition` (form field): Description of plant condition
- `file` (file upload): Image file for the task completion
**Response**: Updated task object with status="completed", image_path, and plant_condition
**Validation**: 
- Only assigned worker can complete
- Task must be in "pending" status
- Image is saved to `uploads/worker_{worker_id}/filename`

## Status Values
- `pending` (default when created)
- `in_progress`
- `completed`

## Frontend Integration Notes

### Create Task Page
- Form fields: title, description, crop_type (dropdown), due_date (date picker), assigned_to (dropdown from workers API)
- POST to `/api/tasks/`
- Default status: pending

### Task List Page
- GET `/api/tasks/` to fetch all tasks
- Display: title, description, crop_type, due_date, worker_name, status (with badges)
- Actions: Edit, Delete buttons
- Status badges: Pending (gray), In Progress (blue), Completed (green)

### Workers Dropdown
- GET `/api/workers/` to get list of workers for assignment
- Use worker.id as assigned_to value

## Files Created/Modified
- `app/models/task.py` - Task model (added image_path, plant_condition)
- `app/schemas/task.py` - Pydantic schemas (added fields to TaskUpdate, Task, TaskWithWorker)
- `app/crud/task.py` - CRUD operations (added complete_task function, updated TaskWithWorker)
- `app/routers/tasks.py` - API endpoints (added complete task endpoint with file upload)
- `app/main.py` - Include tasks router
- `alembic/versions/xxx_create_tasks_table.py` - Migration
- `alembic/versions/ea55724616d2_add_image_path_and_plant_condition_to_tasks.py` - New migration
- `README.md` - Updated documentation