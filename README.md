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

# serial 2

| ধাপ       | কাজ                                         | ফলাফল  |
| --------- | ------------------------------------------- | ------ |
| 🔹 Step 1 | Register → Email পাঠানো                     | ✅ সফল |
| 🔹 Step 2 | Email verification (GET)                    | ✅ সফল |
| 🔹 Step 3 | Login (Session based)                       | ✅ সফল |
| 🔹 Step 4 | Forgot password request → ইমেইলে লিংক       | ✅ সফল |
| 🔹 Step 5 | Password reset confirm → নতুন পাসওয়ার্ড সেট | ✅ সফল |
| 🔹 Step 6 | নতুন পাসওয়ার্ড দিয়ে Login                   | ✅ সফল |

# Learning form serial 2

| বিষয়                         | আপনি কীভাবে শিখলেন                             |
| ---------------------------- | ---------------------------------------------- |
| Django তে ইমেইল ভেরিফিকেশন   | `urlsafe_base64_encode + token_generator` দিয়ে |
| Token Validation             | `check_token()` দিয়ে                           |
| Password Reset Secure Link   | UID + Token সহ URL ব্যবহার করে                 |
| Email পাঠানো                 | `send_mail()` দিয়ে console/backend SMTP        |
| Session-based Authentication | Login → Cookie sessionID                       |
| Postman দিয়ে Full API Test   | Register → Verify → Login → Reset Password ✅  |

✅ Serial 2 Complete: Gmail SMTP setup with real email verification & password reset flow

# from serial 2

✅ Serial 2 থেকে Django-তে যা যা শিখলেন (Easy Points)

# 🔐 Authentication Flow

✅ ইমেইল ভেরিফিকেশন ছাড়া লগইন ব্লক করা (is_active=False)
✅ ইমেইল ভেরিফিকেশন লিংক auto generate করে ইমেইলে পাঠানো

# 📬 Email System

✅ send_mail() দিয়ে ইমেইল পাঠানো
✅ Gmail SMTP সেটআপ করা (App Password সহ)
✅ settings.py ও .env দিয়ে secure email config করা

# 🧾 Token System

✅ Django এর PasswordResetTokenGenerator ব্যবহার করে secure token তৈরি
✅ urlsafe_base64_encode ও decode দিয়ে user ID encode/decode করা
✅ Token + UID সহ ইমেইল লিংক বানানো

# 🔁 Password Reset Flow

✅ “Forgot password” request → ইমেইলে reset link পাঠানো
✅ reset-password-confirm link → নতুন password সেট করা
✅ Token validation handle করে secure password update

# 🧪 API Testing via Postman

✅ Register → Email verify → Login → Reset → Re-login full flow
✅ Bad token, invalid email ইত্যাদি response বুঝে handle করা

# ⚙️ Code Structure

✅ Views: function-based & class-based usage
✅ settings → email config
✅ .env থেকে sensitive data ব্যবহার
🎁 Bonus: Real-World Practice
✅ Gmail-এর মাধ্যমে বাস্তব ইমেইল সিস্টেম কাজ করে দেখেছেন
✅ Development vs Production config বুঝেছেন
✅ Security, Token, Session, SMTP — সব বাস্তবে implement করেছেন
🟢 আপনার দক্ষতা এখন:
🏆 “Production-ready Email Auth System তৈরি করার সম্পূর্ণ যোগ্যতা অর্জন করেছেন”

# 🛡️ Django JWT Authentication API (SimpleJWT)

This project implements a secure authentication system using **Django REST Framework** and **SimpleJWT** for token-based access.

---
