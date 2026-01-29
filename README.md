
# Appbook

## Overview
This project contains 2 Python module(s) with 2 classes and 78 functions/methods.

## Project Structure

### appbook/auth_db.py
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
- `delete_book()`
- `set_category_discount()`
- `get_category_discounts()`
- `get_category_discount()`
- `delete_category_discount()`
- ... and 13 more methods

### appbook/login_app.py
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
- `create_admin_add_book_page()`
- `create_admin_view_books_page()`
- `create_admin_discount_page()`
- `create_admin_user_management_page()`
- `refresh_users_view()`
- ... and 35 more methods

## Installation

```bash
pip install -r requirements.txt
```

## Usage

To use this project:

1. Install dependencies
2. Import the modules in your code
3. Use the classes and functions as needed

## Example

```python
from auth_db import ...
from login_app import ...

# Use the imported classes/functions
```

## File Descriptions

### `appbook/auth_db.py`
Provides:
- 1 class(es)
- 28 function(s)/method(s)

### `appbook/login_app.py`
Provides:
- 1 class(es)
- 50 function(s)/method(s)

## Requirements

This project requires Python 3.7+

## Notes

- Total modules: 2
- Total classes: 2
- Total functions: 78

---
README generated automatically from project code structure.
