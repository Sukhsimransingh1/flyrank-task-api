from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
import os
import psycopg
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")
app = FastAPI(
    title="Task API",
    description="PostgreSQL CRUD API",
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

    conn = psycopg.connect(DATABASE_URL)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, done
        FROM tasks
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
        for row in rows
    ]

# Get Task By ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    conn = psycopg.connect(DATABASE_URL)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = %s
        """,
        (task_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
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

    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING id, title, done
        """,
        (title, False)
    )

    new_task = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": new_task[0],
        "title": new_task[1],
        "done": new_task[2]
    }
# Update Task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id=%s
        """,
        (task_id,)
    )

    task = cursor.fetchone()

    if task is None:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    title = task[1]
    done = task[2]

    if updated_task.title is not None:
        if updated_task.title.strip() == "":
            cursor.close()
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )
        title = updated_task.title.strip()

    if updated_task.done is not None:
        done = updated_task.done

    cursor.execute(
        """
        UPDATE tasks
        SET title=%s,
            done=%s
        WHERE id=%s
        """,
        (title, done, task_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": task_id,
        "title": title,
        "done": done
    }

# Delete Task
@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM tasks WHERE id=%s",
        (task_id,)
    )

    task = cursor.fetchone()

    if task is None:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (task_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)