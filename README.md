# 🚀 Django Project Starter

A modern, scalable Django backend for web applications. Built with best practices for development, deployment, and collaboration.

## 🧾 Features

- Django 4.x / 5.x
- Django REST Framework
- PostgreSQL / SQLite (configurable)
- Environment-based settings (`.env`)
- Modular apps and structure
- JWT Authentication (optional)
- Docker support (optional)

---

## ⚙️ Requirements

- Python 3.10+
- pip / pipx
- Git
- PostgreSQL (if used)
- Virtualenv / venv

---

## 🧱 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-django-project.git
cd your-django-project
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project with the following content:

```ini
DEBUG=True
SECRET_KEY=
DATABASE_URL=


CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
 

PADDLE_CLIENT_SIDE_TOKEN=
PADDLE_API_SECRET_KEY=
# PADDLE_WEBHOOK_SECRET=
PADDLE_WEBHOOK_SECRET=
PADDLE_ENVIRONMENT=

ALLOWED_HOSTS=localhost, 127.0.0.1


EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=


DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=
```

> You can use `sqlite3` by changing `DB_ENGINE=django.db.backends.sqlite3` and commenting out other DB-related lines.

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Visit: [http://localhost:8000](http://localhost:8000)

---



---

## 🛠 Common Commands

```bash
python manage.py makemigrations    # Create new migrations
python manage.py migrate           # Apply migrations
python manage.py createsuperuser   # Create admin user
python manage.py collectstatic     # Collect static files
```




---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License. See [`LICENSE`](LICENSE) for details.