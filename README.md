# TASKS PRO – Team Task Management System

A full-stack web application for managing team tasks with role-based access control, built with Django and a modern dark-mode UI.

---

## Features

- **Role-based access** – Admin users can create, edit, and delete tasks; regular users can self-assign and update task status
- **Team management** – Users are assigned to teams and see only their team's tasks
- **Task lifecycle** – Track tasks from `New` → `In Progress` → `Completed`
- **Modern UI** – Dark-mode design with Tailwind CSS, glassmorphism effects, and RTL (Hebrew) support
- **Authentication** – Secure login/register system using Django's built-in auth
- **Filtering** – Filter tasks by status and assigned executor

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django 6 |
| Frontend | HTML, Tailwind CSS |
| Database | SQLite |
| Auth | Django Authentication |

---

## Project Structure

```
myProject/
├── myProject/          # Project settings & URLs
├── DjangoApp/          # Main application
│   ├── models.py       # Team, Person, Task models
│   ├── views.py        # All view logic
│   ├── forms.py        # Form definitions
│   └── urls.py         # URL routing
├── Templates/          # HTML templates
├── requirements.txt
└── manage.py
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/l8810/Project_Python.git
cd Project_Python/myProject
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Start the server

```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000**

---

## Usage

| Role | Permissions |
|------|------------|
| **Admin** | Create / Edit / Delete tasks, view all team tasks |
| **User** | View tasks, self-assign unassigned tasks, update status if assigned |

1. Register a new account and select your team
2. Log in to view your team's task board
3. Admins can add new tasks from the dashboard
4. Users can claim unassigned tasks and update their progress

---

## Screenshots

> Dashboard – Task Board

![Tasks Dashboard](https://via.placeholder.com/800x400?text=Tasks+Dashboard)

> Registration Page

![Register](https://via.placeholder.com/800x400?text=Register+Page)

---

## License

This project is open source and available under the [MIT License](LICENSE).
