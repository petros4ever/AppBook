import sqlite3
import hashlib
import os
from pathlib import Path

class AuthDatabase:
    """Database manager for user authentication"""
    
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin')),
                is_banned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add role column if it doesn't exist (migration for existing databases)
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'role' not in columns:
            cursor.execute('''
                ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin'))
            ''')
        
        if 'is_banned' not in columns:
            cursor.execute('''
                ALTER TABLE users ADD COLUMN is_banned INTEGER DEFAULT 0
            ''')
        
        conn.commit()
        
        # Create default admin if it doesn't exist
        self._create_default_admin(cursor, conn)
        
        # Create books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL DEFAULT 0.0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add price column if it doesn't exist (migration for existing databases)
        cursor.execute("PRAGMA table_info(books)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'price' not in columns:
            cursor.execute('''
                ALTER TABLE books ADD COLUMN price REAL NOT NULL DEFAULT 0.0
            ''')
        
        if 'content' not in columns:
            cursor.execute('''
                ALTER TABLE books ADD COLUMN content TEXT DEFAULT ''
            ''')
        
        conn.commit()
        
        # Create category_discounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category_discounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                discount_percentage REAL NOT NULL CHECK(discount_percentage >= 0 AND discount_percentage <= 100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create purchases table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                purchase_price REAL NOT NULL,
                discount_applied REAL DEFAULT 0,
                final_price REAL NOT NULL,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')
        
        # Create reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                rating INTEGER DEFAULT NULL,
                review_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')

        # Create notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_id INTEGER,
                message TEXT NOT NULL,
                is_broadcast INTEGER DEFAULT 1,
                target_user_id INTEGER DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (actor_id) REFERENCES users(id),
                FOREIGN KEY (target_user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()
    
    def _create_default_admin(self, cursor, conn):
        """Create default admin user if not exists"""
        cursor.execute('SELECT * FROM users WHERE role = ?', ('admin',))
        if cursor.fetchone() is None:
            # No admin exists, create default admin
            admin_username = "admin"
            admin_email = "admin@system.local"
            admin_password = "admin123"  # Default password for first setup
            
            password_hash = self.hash_password(admin_password)
            try:
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (?, ?, ?, ?)
                ''', (admin_username, admin_email, password_hash, 'admin'))
                conn.commit()
                print(f"Default admin created - Username: {admin_username}, Password: {admin_password}")
            except sqlite3.IntegrityError:
                # Admin might already exist
                pass
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if username or email already exists
            cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
                          (username, email))
            if cursor.fetchone():
                return False, "Username or email already exists"
            
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            
            conn.commit()
            conn.close()
            return True, "User registered successfully"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def login_user(self, username, password):
        """Verify user login credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute('''
                SELECT id, username, email, role FROM users 
                WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return True, user  # Returns (success, (id, username, email, role))
            else:
                return False, "Invalid username or password"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def user_exists(self, username):
        """Check if username exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    # Book management methods
    
    def add_book(self, title, author, category, price, description="", content=""):
        """Add a new book to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO books (title, author, category, price, description, content)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, author, category, price, description, content))
            
            conn.commit()
            conn.close()
            return True, "Book added successfully"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def get_all_books(self):
        """Get all books from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, author, category, price, description, created_at
                FROM books
                ORDER BY category, title
            ''')
            
            books = cursor.fetchall()
            conn.close()
            return True, books
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def get_books_by_category(self):
        """Get books organized by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT category FROM books
                ORDER BY category
            ''')
            
            categories = [row[0] for row in cursor.fetchall()]
            books_by_category = {}
            
            for category in categories:
                cursor.execute('''
                    SELECT id, title, author, price, description
                    FROM books
                    WHERE category = ?
                    ORDER BY title
                ''', (category,))
                books_by_category[category] = cursor.fetchall()
            
            conn.close()
            return True, books_by_category
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def delete_book(self, book_id):
        """Delete a book from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            
            conn.commit()
            conn.close()
            return True, "Book deleted successfully"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    # Discount management methods
    
    def set_category_discount(self, category, discount_percentage):
        """Set or update discount for a category"""
        try:
            if discount_percentage < 0 or discount_percentage > 100:
                return False, "Discount must be between 0 and 100"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if discount already exists
            cursor.execute('SELECT id FROM category_discounts WHERE category = ?', (category,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing discount
                cursor.execute('''
                    UPDATE category_discounts 
                    SET discount_percentage = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE category = ?
                ''', (discount_percentage, category))
                message = "Discount updated successfully"
            else:
                # Insert new discount
                cursor.execute('''
                    INSERT INTO category_discounts (category, discount_percentage)
                    VALUES (?, ?)
                ''', (category, discount_percentage))
                message = "Discount added successfully"
            
            conn.commit()
            conn.close()
            return True, message
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def get_category_discounts(self):
        """Get all category discounts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, category, discount_percentage, updated_at
                FROM category_discounts
                ORDER BY category
            ''')
            
            discounts = cursor.fetchall()
            conn.close()
            return True, discounts
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def get_category_discount(self, category):
        """Get discount for a specific category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT discount_percentage FROM category_discounts
                WHERE category = ?
            ''', (category,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return True, result[0]
            else:
                return True, 0  # No discount
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def delete_category_discount(self, category):
        """Delete discount for a category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM category_discounts WHERE category = ?', (category,))
            
            conn.commit()
            conn.close()
            return True, "Discount removed successfully"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    # User management methods
    
    def get_all_users(self):
        """Get all non-admin users"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, is_banned, created_at
                FROM users
                WHERE role = 'user'
                ORDER BY username
            ''')
            
            users = cursor.fetchall()
            conn.close()
            return True, users
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def ban_user(self, user_id):
        """Ban a user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('UPDATE users SET is_banned = 1 WHERE id = ? AND role = ?', 
                          (user_id, 'user'))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "User not found or cannot ban this user"
            
            conn.commit()
            conn.close()
            return True, "User banned successfully"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def unban_user(self, user_id):
        """Unban a user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('UPDATE users SET is_banned = 0 WHERE id = ? AND role = ?', 
                          (user_id, 'user'))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "User not found or cannot unban this user"
            
            conn.commit()
            conn.close()
            return True, "User unbanned successfully"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def is_user_banned(self, username):
        """Check if a user is banned"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT is_banned FROM users WHERE username = ?', (username,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0] == 1
            return False
        
        except sqlite3.Error as e:
            return False
    
    def search_books(self, search_query):
        """Search books by title, author, or category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Search with wildcard pattern
            search_pattern = f"%{search_query}%"
            
            cursor.execute('''
                SELECT id, title, author, category, price, description
                FROM books
                WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
                ORDER BY category, title
            ''', (search_pattern, search_pattern, search_pattern))
            
            books = cursor.fetchall()
            conn.close()
            return True, books
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    # Purchase management methods
    
    def purchase_book(self, user_id, book_id):
        """Record a book purchase for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get book details and price
            cursor.execute('SELECT title, category, price FROM books WHERE id = ?', (book_id,))
            book_result = cursor.fetchone()
            
            if not book_result:
                conn.close()
                return False, "Book not found"
            
            title, category, price = book_result
            
            # Check if user already bought this book
            cursor.execute('''
                SELECT id FROM purchases 
                WHERE user_id = ? AND book_id = ?
            ''', (user_id, book_id))
            
            if cursor.fetchone():
                conn.close()
                return False, "You have already purchased this book"
            
            # Get discount for this category
            cursor.execute('''
                SELECT discount_percentage FROM category_discounts
                WHERE category = ?
            ''', (category,))
            
            discount_result = cursor.fetchone()
            discount_percentage = discount_result[0] if discount_result else 0
            
            # Calculate final price
            discount_amount = price * (discount_percentage / 100)
            final_price = price - discount_amount
            
            # Record the purchase
            cursor.execute('''
                INSERT INTO purchases (user_id, book_id, purchase_price, discount_applied, final_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, book_id, price, discount_amount, final_price))
            
            conn.commit()
            conn.close()
            
            return True, f"Successfully purchased '{title}' for ${final_price:.2f}"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def get_user_purchases(self, user_id):
        """Get all purchases for a specific user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.id, b.title, b.author, b.category, p.purchase_price, 
                       p.discount_applied, p.final_price, p.purchase_date
                FROM purchases p
                JOIN books b ON p.book_id = b.id
                WHERE p.user_id = ?
                ORDER BY p.purchase_date DESC
            ''', (user_id,))
            
            purchases = cursor.fetchall()
            conn.close()
            return True, purchases
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def get_book_by_id(self, book_id):
        """Get book details by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, author, category, price, description, content
                FROM books
                WHERE id = ?
            ''', (book_id,))
            
            book = cursor.fetchone()
            conn.close()
            return True, book
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def get_book_content(self, book_id):
        """Get book content for reading"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title, author, content
                FROM books
                WHERE id = ?
            ''', (book_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return True, result
            else:
                return False, "Book not found"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    # Review management methods

    def add_review(self, user_id, book_id, review_text, rating=None):
        """Add a review for a book by a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Optionally ensure book exists
            cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
            if cursor.fetchone() is None:
                conn.close()
                return False, "Book not found"

            # Insert review
            cursor.execute('''
                INSERT INTO reviews (user_id, book_id, rating, review_text)
                VALUES (?, ?, ?, ?)
            ''', (user_id, book_id, rating, review_text))

            conn.commit()
            conn.close()
            return True, "Review submitted successfully"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def get_reviews_for_book(self, book_id):
        """Retrieve all reviews for a given book, including reviewer username"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT r.id, r.user_id, u.username, r.rating, r.review_text, r.created_at
                FROM reviews r
                JOIN users u ON r.user_id = u.id
                WHERE r.book_id = ?
                ORDER BY r.created_at DESC
            ''', (book_id,))

            reviews = cursor.fetchall()
            conn.close()
            return True, reviews

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    # Notifications methods

    def add_notification(self, actor_id, message, broadcast=True, target_user_id=None):
        """Add a notification. If broadcast=True it targets all users, otherwise target_user_id must be set."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            is_broadcast = 1 if broadcast else 0
            cursor.execute('''
                INSERT INTO notifications (actor_id, message, is_broadcast, target_user_id)
                VALUES (?, ?, ?, ?)
            ''', (actor_id, message, is_broadcast, target_user_id))

            conn.commit()
            conn.close()
            return True, "Notification created"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def get_notifications_for_user(self, user_id, limit=100):
        """Retrieve notifications visible to a given user (broadcasts + targeted)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT n.id, n.actor_id, u.username as actor_username, n.message, n.is_broadcast, n.target_user_id, n.created_at
                FROM notifications n
                LEFT JOIN users u ON n.actor_id = u.id
                WHERE n.is_broadcast = 1 OR n.target_user_id = ?
                ORDER BY n.created_at DESC
                LIMIT ?
            ''', (user_id, limit))

            notes = cursor.fetchall()
            conn.close()
            return True, notes

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
