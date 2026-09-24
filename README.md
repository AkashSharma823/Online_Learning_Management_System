# Heartify — Online Learning Management System

A full-stack Heartify LMS project using React + TypeScript on the frontend and Django REST Framework + MySQL on the backend.

## Stack

### Frontend
- React.js + TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React
- FullCalendar
- React Player 3

### Backend
- Python 3.11+
- Django 5.2
- Django REST Framework
- SimpleJWT
- MySQL (mysqlclient driver)

## Important fixes included
- Fixed nested role-route matching by using relative child routes.
- Added missing Vite type declarations (`src/vite-env.d.ts`).
- Updated React Player usage from `url` to the v3 `src` prop.
- Removed the unsafe frontend "accept any login when the API is down" fallback.
- Registration now reports real API errors instead of redirecting on failure.
- Added profile routes for student, instructor and admin dashboards.
- Added a complete initial Django migration for the LMS models.
- Switched the MySQL driver from PyMySQL to mysqlclient (MySQLdb), including the dependency and setup instructions.
- Improved email/username registration validation and API-owned fields.

## Run on Windows

### 1. MySQL

Create the database:

```sql
CREATE DATABASE heartify_lms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Backend: http://127.0.0.1:8000

### mysqlclient on Windows

This project uses `mysqlclient` (the `MySQLdb` Django backend) instead of PyMySQL. If `pip install -r requirements.txt` cannot find a compatible `mysqlclient` wheel on your Python version, use Python 3.11 64-bit and make sure the Microsoft C++ Build Tools and MySQL/MariaDB development libraries are available.

### 3. Frontend

Open a second terminal:

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend: http://127.0.0.1:5173

## Demo users

- Admin: `admin@heartify.com` / `Admin@123`
- Instructor: `instructor@heartify.com` / `Instructor@123`
- Student: `student@heartify.com` / `Student@123`


