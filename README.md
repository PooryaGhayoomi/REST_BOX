# 🏡 RestBox API

Welcome to **RestBox**! 👋

RestBox is a simple RESTful API for an online villa reservation system, built with **Django** and **Django REST Framework**. It allows users to register, manage villas, make reservations, and verify payments through secure APIs.

## ✨ Features

- 🔐 JWT Authentication
- 👤 Host & Guest roles
- 🏠 Villa management
- 📅 Availability management
- 📝 Reservation system
- 💳 Payment verification

## 🛠️ Built With

- Python
- Django
- Django REST Framework
- SQLite
- Simple JWT

## 🚀 Getting Started

Clone the repository:

```bash
git clone <repository-url>
cd RestBox
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

## 📌 Main Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `GET /api/villas/`
- `POST /api/villas/`
- `GET /api/reservations/history/`
- `POST /api/reservations/`
- `POST /api/payments/verify/`

## 🔑 Authentication

Protected endpoints require a JWT access token:

```
Authorization: Bearer <access_token>
```

---

Made with ❤️ using Django & DRF.
