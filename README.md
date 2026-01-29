# Appbook Project - Book Management System

## Overview
Appbook is a comprehensive book management and reader application built with PySide6. It provides user authentication, book browsing, purchasing, reading, and review capabilities.

## Features
- User authentication and registration
- Admin panel for book and user management
- Book browsing by category with search functionality
- Book purchasing with discount management
- Book reader with content display
- User reviews and ratings system
- User and admin notifications
- Ban/unban user management
- Category-based discount system

## Project Structure

### appbook\auth_db.py
**Classes:**
- `AuthDatabase`

**Functions/Methods:**
- `__init__()`
- `init_database()`
- `_create_default_admin()`
- `hash_password()`
- `register_user()`
- `login_user()`
- `user_exists()`
- `add_book()`
- `get_all_books()`
- `get_books_by_category()`
- ... and 18 more methods

### appbook\login_app.py
**Classes:**
- `LoginSignupApp`

**Functions/Methods:**
- `main()`
- `__init__()`
- `init_ui()`
- `create_login_page()`
- `create_signup_page()`
- `create_dashboard_page()`
- `create_user_books_page()`
- `create_user_purchases_page()`
- `create_book_reader_page()`
- `create_admin_dashboard_page()`
- ... and 40 more methods

## Installation

```bash
pip install PySide6
```

## Usage

Run the application:
```bash
python login_app.py
```

### Default Admin Credentials
- Username: `admin`
- Password: `admin123`

## Module Details

### auth_db.py
Database management module handling:
- User authentication and registration
- Book management (add, delete, search)
- Purchase tracking and discount management
- Reviews and notifications
- User ban/unban functionality

### login_app.py
Main UI application built with PySide6 providing:
- Login and signup pages
- User dashboard with book browsing
- Admin dashboard with management tools
- Book reader interface
- Notification system
- Review submission and display

## Database
SQLite database (`users.db`) with tables:
- `users` - User accounts and authentication
- `books` - Book catalog
- `purchases` - Purchase history
- `category_discounts` - Discount settings
- `reviews` - Book reviews and ratings
- `notifications` - System notifications

## Key Features in Detail

### User System
- Create accounts with email and password
- Login with credentials
- User banning by admin
- Role-based access (user/admin)

### Admin Features
- Add new books with content
- Delete books
- Manage category discounts
- View and manage users
- Ban/unban users
- View books with reviews

### User Features
- Browse books by category
- Search books
- Purchase books
- Read purchased books
- Submit reviews and ratings
- View notifications

## Running the Application

1. Ensure all dependencies are installed
2. Run `python login_app.py`
3. Login as admin (admin/admin123) or create a new account
4. Explore the features

## Database Schema
The application automatically creates and initializes the SQLite database on first run.
All tables are created with appropriate indexes and foreign key relationships.

---
Generated automatically from project code structure.
