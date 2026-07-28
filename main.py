from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
import os
import psycopg
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="Task API",
    description="SQLite CRUD API",
    version="2.0"
)




# Request Models
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# Database Initialization
def init_db():
    conn = psycopg.connect(DATABASE_URL)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")

    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            """,
            [
                ("Learn FastAPI", False),
                ("Complete FlyRank Assignment", False),
                ("Practice Python", True),
            ]
        )

    conn.commit()

    cursor.close()
    conn.close()

init_db()


# Root
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "endpoints": ["/tasks"]
    }


# Health
@app.get("/health")
def health():
    return {"status": "ok"}


# Get All Tasks
@app.get("/tasks")
def get_tasks():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]


# Get Task By ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


# Create Task
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):

    title = task.title.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, 0)
    )

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return {
        "id": new_id,
        "title": title,
        "done": False
    }


# Update Task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    task = cursor.fetchone()

    if task is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    title = task["title"]
    done = task["done"]

    if updated_task.title is not None:
        if updated_task.title.strip() == "":
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )
        title = updated_task.title.strip()

    if updated_task.done is not None:
        done = int(updated_task.done)

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (title, done, task_id)
    )

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": title,
        "done": bool(done)
    }


# Delete Task
@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    task = cursor.fetchone()

    if task is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)