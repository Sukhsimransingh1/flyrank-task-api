# 🚀 FlyRank Task API

A production-ready **Task Management REST API** built with **FastAPI** and **PostgreSQL**. The application provides complete CRUD functionality with persistent database storage and can be deployed locally or using **Docker Compose** with a single command.

---

## ✨ Features

- ✅ Create tasks
- ✅ Retrieve all tasks
- ✅ Retrieve a task by ID
- ✅ Update existing tasks
- ✅ Delete tasks
- ✅ PostgreSQL persistent storage
- ✅ Automatic database initialization & seeding
- ✅ Dockerized application
- ✅ Docker Compose support
- ✅ Interactive Swagger UI documentation
- ✅ Health Check endpoint

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL 16 |
| Database Driver | Psycopg 3 |
| Validation | Pydantic |
| API Server | Uvicorn |
| Containerization | Docker |
| Orchestration | Docker Compose |

---

# 📂 Project Structure

```text
flyrank-task-api/
│
├── images/
│   ├── swagger-ui.png
│   ├── postgres-db.png
│   └── docker-containers.png
│
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚡ Quick Start (Docker)

Clone the repository

```bash
git clone https://github.com/Sukhsimransingh1/flyrank-task-api.git
cd flyrank-task-api
```

Start the complete application

```bash
docker compose up --build
```

The application will be available at

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

Stop the application

```bash
docker compose down
```

---

# 💻 Local Development

Clone the repository

```bash
git clone https://github.com/Sukhsimransingh1/flyrank-task-api.git
cd flyrank-task-api
```

Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

Run the API

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# 📌 API Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

---

# 📥 Example Request

### Create Task

**POST** `/tasks`

```json
{
    "title": "Learn Docker"
}
```

### Response

```json
{
    "id": 4,
    "title": "Learn Docker",
    "done": false
}
```

---

# 🗄 Database

The application uses **PostgreSQL** as its primary database.

On startup, the application automatically:

- Creates the `tasks` table (if it does not already exist)
- Inserts three sample tasks when the table is empty
- Persists all task data using Docker volumes

Example query

```sql
SELECT * FROM tasks;
```

---

# 🐳 Docker Services

The project uses Docker Compose to manage two services.

| Service | Description |
|----------|-------------|
| PostgreSQL | Database |
| FastAPI | REST API |

Start everything with a single command

```bash
docker compose up --build
```

---

# 📸 Screenshots

## Swagger UI

![Swagger UI](images/swagger-ui.png)

---

## PostgreSQL Database

![PostgreSQL Database](images/postgres-db.png)

---


# 🚀 Future Improvements

- User Authentication (JWT)
- Pagination
- Search & Filtering
- Unit & Integration Testing
- CI/CD Pipeline
- Cloud Deployment (AWS / Azure / Render)
- Logging & Monitoring

---

# 👨‍💻 Author

**Sukhsimran Singh**

GitHub  
https://github.com/Sukhsimransingh1

LinkedIn  
https://www.linkedin.com/in/sukhsimran-singh/

---

## ⭐ If you found this project helpful, consider giving it a star.