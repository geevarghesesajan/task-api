# BE-02: Task Manager API with SQLite Persistence

This is a FastAPI REST API for managing tasks, connected to an SQLite database (`tasks.db`) for persistent storage.

## Database Choice
- **Database:** SQLite 3
- **Reason:** SQLite is lightweight, serverless, and stores data in a single local file (`tasks.db`), making it ideal for fast development and simple persistence without requiring external database servers.

## Database Schema
The API uses a single table named `tasks`:

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto Increment) |
| `title` | TEXT | Title of the task (Required) |
| `done` | BOOLEAN | Completion status (Default: `0` / `False`) |

## How to Run the Project

1. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn