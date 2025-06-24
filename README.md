# Django Auth Project 🔐

A simple Django-based authentication API with PostgreSQL, JWT, and custom user model.

---

## 🚀 Features

- ✅ Custom User Model (Email-based)
- ✅ JWT Authentication (Login, Refresh)
- ✅ PostgreSQL Integration
- ✅ Environment Variable Config via `.env`
- ✅ API Ready for Frontend Integration

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/django-auth-project.git
cd django-auth-project
```

### 1. Done

| কাজ                                                               | স্টেটাস |
| ----------------------------------------------------------------- | ------- |
| ✅ Custom User Model (`AbstractBaseUser` + `PermissionsMixin`)    | ✅ Done |
| ✅ Custom UserManager (`create_user`, `create_superuser`)         | ✅ Done |
| ✅ PostgreSQL integration & `.env` config                         | ✅ Done |
| ✅ Registration API (DRF `CreateAPIView`)                         | ✅ Done |
| ✅ Login API (DRF `APIView` + `login`)                            | ✅ Done |
| ✅ Logout API (DRF `APIView` + `logout`)                          | ✅ Done |
| ✅ CSRF Exempt করে Postman test সম্পন্ন                           | ✅ Done |
| ✅ GitHub push + `.gitignore`, `README.md`, `requirements.txt` সহ | ✅ Done |

# Serial 1 Summary: User Registration, Login, Logout + ToDo App with Auth

📌 Project Requirements (Serial 1):

Feature

Description

Status

Custom User Model

Using AbstractBaseUser, PermissionsMixin, and CustomUserManager

✅ Done

User Registration

API to register users

✅ Done

User Login

API to log in users using DRF + session-based login

✅ Done

User Logout

API to logout authenticated users

✅ Done

View Users

Admin/staff can view all, user can view only their info

✅ Done

Update Own Info

Users can update their own info

✅ Done

Delete Own Account

Users can delete their own account

✅ Done

DRF ViewSet

Used for user-related views (ModelViewSet)

✅ Done

ToDo Model

Linked to User, has fields like title, description, completed, created_at

✅ Done

ToDo List & Create API

Authenticated users can view & create their todos

✅ Done

ToDo Detail API

Retrieve, update, delete specific todos for owner only

✅ Done

Permissions Applied

All views protected with IsAuthenticated

✅ Done

Postman Tested

Manually tested using Postman including auth headers

✅ Done

Project Structure

Django project split into accounts/ and todo/ apps

✅ Done
