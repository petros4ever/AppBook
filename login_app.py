import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox, QFrame,
    QScrollArea, QTextEdit, QComboBox, QListWidget, QListWidgetItem
)
from PySide6.QtWidgets import QDialog, QFormLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from auth_db import AuthDatabase


class LoginSignupApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = AuthDatabase()
        self.current_user = None
        self.user_role = None  # 'admin' or 'user'
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle("Login & Sign Up")
        self.setGeometry(100, 100, 500, 400)
        self.setMinimumSize(500, 400)
        
        # Create stacked widget to switch between login and signup
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create login and signup pages
        self.login_page = self.create_login_page()
        self.signup_page = self.create_signup_page()
        self.dashboard_page = self.create_dashboard_page()
        self.user_books_page = self.create_user_books_page()
        self.admin_dashboard_page = self.create_admin_dashboard_page()
        self.admin_add_book_page = self.create_admin_add_book_page()
        self.admin_view_books_page = self.create_admin_view_books_page()
        self.admin_discount_page = self.create_admin_discount_page()
        self.admin_user_management_page = self.create_admin_user_management_page()
        self.user_purchases_page = self.create_user_purchases_page()
        self.book_reader_page = self.create_book_reader_page()
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.user_books_page)
        self.stacked_widget.addWidget(self.admin_dashboard_page)
        self.stacked_widget.addWidget(self.admin_add_book_page)
        self.stacked_widget.addWidget(self.admin_view_books_page)
        self.stacked_widget.addWidget(self.admin_discount_page)
        self.stacked_widget.addWidget(self.admin_user_management_page)
        self.stacked_widget.addWidget(self.user_purchases_page)
        self.stacked_widget.addWidget(self.book_reader_page)
        
        # Show login page by default
        self.stacked_widget.setCurrentIndex(0)
        
        # Apply stylesheet
        self.apply_stylesheet()
    
    def create_login_page(self):
        """Create login page"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Login")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Username input
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 10))
        layout.addWidget(username_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        self.login_username.setMinimumHeight(40)
        layout.addWidget(self.login_username)
        
        # Password input
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 10))
        layout.addWidget(password_label)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setMinimumHeight(40)
        layout.addWidget(self.login_password)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.setMinimumHeight(40)
        login_btn.setFont(QFont("Arial", 11, QFont.Bold))
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        # Signup link
        signup_text = QLabel("Don't have an account? ")
        signup_btn = QPushButton("Sign Up")
        signup_btn.setMaximumWidth(80)
        signup_btn.clicked.connect(lambda: self.show_page(1))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(signup_text)
        button_layout.addWidget(signup_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_signup_page(self):
        """Create signup page"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Create Account")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Username input
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 10))
        layout.addWidget(username_label)
        
        self.signup_username = QLineEdit()
        self.signup_username.setPlaceholderText("Choose a username (3-20 characters)")
        self.signup_username.setMinimumHeight(40)
        layout.addWidget(self.signup_username)
        
        # Email input
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 10))
        layout.addWidget(email_label)
        
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Enter your email")
        self.signup_email.setMinimumHeight(40)
        layout.addWidget(self.signup_email)
        
        # Password input
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 10))
        layout.addWidget(password_label)
        
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Enter password (min 6 characters)")
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.setMinimumHeight(40)
        layout.addWidget(self.signup_password)
        
        # Confirm password input
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setFont(QFont("Arial", 10))
        layout.addWidget(confirm_label)
        
        self.signup_confirm_password = QLineEdit()
        self.signup_confirm_password.setPlaceholderText("Confirm your password")
        self.signup_confirm_password.setEchoMode(QLineEdit.Password)
        self.signup_confirm_password.setMinimumHeight(40)
        layout.addWidget(self.signup_confirm_password)
        
        # Signup button
        signup_btn = QPushButton("Sign Up")
        signup_btn.setMinimumHeight(40)
        signup_btn.setFont(QFont("Arial", 11, QFont.Bold))
        signup_btn.clicked.connect(self.handle_signup)
        layout.addWidget(signup_btn)
        
        # Login link
        login_text = QLabel("Already have an account? ")
        login_btn = QPushButton("Login")
        login_btn.setMaximumWidth(80)
        login_btn.clicked.connect(lambda: self.show_page(0))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(login_text)
        button_layout.addWidget(login_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_dashboard_page(self):
        """Create dashboard page after successful login"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Welcome message
        self.welcome_label = QLabel()
        self.welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.welcome_label)
        
        # User info
        self.user_info_label = QLabel()
        self.user_info_label.setFont(QFont("Arial", 12))
        self.user_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.user_info_label)
        
        layout.addStretch()
        
        # View Books button
        books_btn = QPushButton("View Books")
        books_btn.setMinimumHeight(40)
        books_btn.setFont(QFont("Arial", 11, QFont.Bold))
        books_btn.clicked.connect(self.show_user_books_view)
        layout.addWidget(books_btn)
        
        # Notifications button
        self.notifications_btn = QPushButton("Notifications")
        self.notifications_btn.setMinimumHeight(40)
        self.notifications_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.notifications_btn.clicked.connect(self.show_notifications)
        layout.addWidget(self.notifications_btn)
        
        # View Purchases button
        purchases_btn = QPushButton("My Purchases")
        purchases_btn.setMinimumHeight(40)
        purchases_btn.setFont(QFont("Arial", 11, QFont.Bold))
        purchases_btn.clicked.connect(self.show_user_purchases)
        layout.addWidget(purchases_btn)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setMinimumHeight(40)
        logout_btn.setFont(QFont("Arial", 11, QFont.Bold))
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        page.setLayout(layout)
        return page
    
    def create_user_books_page(self):
        """Create page for users to browse books by category"""
        page = QWidget()
        main_layout = QHBoxLayout()
        
        # Left sidebar with categories
        left_layout = QVBoxLayout()
        left_frame = QFrame()
        left_frame.setMinimumWidth(200)
        left_frame.setMaximumWidth(250)
        
        cat_label = QLabel("Categories")
        cat_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(cat_label)
        
        self.user_category_list = QListWidget()
        self.user_category_list.itemClicked.connect(self.on_user_category_selected)
        left_layout.addWidget(self.user_category_list)
        
        left_frame.setLayout(left_layout)
        main_layout.addWidget(left_frame)
        
        # Right side with books
        right_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Books Available")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        # Search bar
        search_layout = QHBoxLayout()
        
        search_label = QLabel("Search Books:")
        search_label.setFont(QFont("Arial", 10))
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, or category...")
        self.search_input.setMinimumHeight(35)
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Search")
        search_btn.setMinimumHeight(35)
        search_btn.setMaximumWidth(80)
        search_btn.clicked.connect(self.handle_search_books)
        search_layout.addWidget(search_btn)
        
        clear_search_btn = QPushButton("Clear")
        clear_search_btn.setMinimumHeight(35)
        clear_search_btn.setMaximumWidth(80)
        clear_search_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(clear_search_btn)
        
        right_layout.addLayout(search_layout)
        
        # Books display
        self.user_books_display = QListWidget()
        self.user_books_display.itemClicked.connect(self.on_user_book_selected)
        right_layout.addWidget(self.user_books_display)
        
        # Buy button (initially hidden)
        self.buy_book_btn = QPushButton("Buy Selected Book")
        self.buy_book_btn.setMinimumHeight(35)
        self.buy_book_btn.setVisible(False)
        self.buy_book_btn.clicked.connect(self.handle_buy_book)
        right_layout.addWidget(self.buy_book_btn)

        # View Info button (initially hidden)
        self.view_info_btn = QPushButton("View Info")
        self.view_info_btn.setMinimumHeight(35)
        self.view_info_btn.setVisible(False)
        self.view_info_btn.clicked.connect(self.handle_view_book_info)
        right_layout.addWidget(self.view_info_btn)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.clicked.connect(self.refresh_user_books_view)
        button_layout.addWidget(refresh_btn)
        
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setMinimumHeight(35)
        back_btn.clicked.connect(lambda: self.show_page(2))
        button_layout.addWidget(back_btn)
        
        right_layout.addLayout(button_layout)
        
        right_frame = QFrame()
        right_frame.setLayout(right_layout)
        main_layout.addWidget(right_frame, 1)
        
        page.setLayout(main_layout)
        return page
    
    def create_user_purchases_page(self):
        """Create page to view user's purchased books"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("My Purchases")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Purchases display
        self.user_purchases_display = QListWidget()
        self.user_purchases_display.itemClicked.connect(self.on_purchase_selected)
        layout.addWidget(self.user_purchases_display)
        
        # Read button (initially hidden)
        self.read_book_btn = QPushButton("Read Selected Book")
        self.read_book_btn.setMinimumHeight(35)
        self.read_book_btn.setVisible(False)
        self.read_book_btn.clicked.connect(self.handle_read_book)
        layout.addWidget(self.read_book_btn)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.clicked.connect(self.refresh_purchases_view)
        button_layout.addWidget(refresh_btn)
        
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setMinimumHeight(35)
        back_btn.clicked.connect(lambda: self.show_page(2))
        button_layout.addWidget(back_btn)
        
        layout.addLayout(button_layout)
        
        page.setLayout(layout)
        return page
    
    def create_book_reader_page(self):
        """Create page for reading books"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Title bar
        title_layout = QHBoxLayout()
        self.reader_book_title = QLabel()
        self.reader_book_title.setFont(QFont("Arial", 16, QFont.Bold))
        title_layout.addWidget(self.reader_book_title)
        
        self.reader_book_author = QLabel()
        self.reader_book_author.setFont(QFont("Arial", 11))
        self.reader_book_author.setAlignment(Qt.AlignRight)
        title_layout.addWidget(self.reader_book_author)
        
        layout.addLayout(title_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        layout.addWidget(separator)
        
        # Book content display
        self.book_content_display = QTextEdit()
        self.book_content_display.setReadOnly(True)
        self.book_content_display.setFont(QFont("Arial", 11))
        layout.addWidget(self.book_content_display)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        back_btn = QPushButton("Back to Purchases")
        back_btn.setMinimumHeight(35)
        back_btn.clicked.connect(lambda: self.show_page(9))
        button_layout.addWidget(back_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        page.setLayout(layout)
        return page
    
    def create_admin_dashboard_page(self):
        """Create admin dashboard page"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Welcome message
        self.admin_welcome_label = QLabel()
        self.admin_welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.admin_welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.admin_welcome_label)
        
        # Admin info
        self.admin_info_label = QLabel()
        self.admin_info_label.setFont(QFont("Arial", 12))
        self.admin_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.admin_info_label)
        
        # Admin options
        admin_title = QLabel("Admin Panel")
        admin_title.setFont(QFont("Arial", 14, QFont.Bold))
        admin_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(admin_title)
        
        # Add Book button
        add_book_btn = QPushButton("Add New Book")
        add_book_btn.setMinimumHeight(40)
        add_book_btn.setFont(QFont("Arial", 11))
        add_book_btn.clicked.connect(lambda: self.show_page(5))
        layout.addWidget(add_book_btn)
        
        # View Books button
        view_books_btn = QPushButton("View Books by Category")
        view_books_btn.setMinimumHeight(40)
        view_books_btn.setFont(QFont("Arial", 11))
        view_books_btn.clicked.connect(lambda: self.show_admin_books_view())
        layout.addWidget(view_books_btn)
        
        # Manage Discounts button
        discount_btn = QPushButton("Manage Category Discounts")
        discount_btn.setMinimumHeight(40)
        discount_btn.setFont(QFont("Arial", 11))
        discount_btn.clicked.connect(lambda: self.show_discount_management())
        layout.addWidget(discount_btn)
        
        # Manage users button (placeholder)
        manage_users_btn = QPushButton("Manage Users")
        manage_users_btn.setMinimumHeight(40)
        manage_users_btn.setFont(QFont("Arial", 11))
        manage_users_btn.clicked.connect(self.show_users_management)
        layout.addWidget(manage_users_btn)
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setMinimumHeight(40)
        logout_btn.setFont(QFont("Arial", 11, QFont.Bold))
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        page.setLayout(layout)
        return page
    
    def create_admin_add_book_page(self):
        """Create page for adding new books"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Add New Book")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Book title
        title_label = QLabel("Book Title:")
        title_label.setFont(QFont("Arial", 10))
        layout.addWidget(title_label)
        
        self.book_title_input = QLineEdit()
        self.book_title_input.setPlaceholderText("Enter book title")
        self.book_title_input.setMinimumHeight(35)
        layout.addWidget(self.book_title_input)
        
        # Author
        author_label = QLabel("Author:")
        author_label.setFont(QFont("Arial", 10))
        layout.addWidget(author_label)
        
        self.book_author_input = QLineEdit()
        self.book_author_input.setPlaceholderText("Enter author name")
        self.book_author_input.setMinimumHeight(35)
        layout.addWidget(self.book_author_input)
        
        # Category
        category_label = QLabel("Category:")
        category_label.setFont(QFont("Arial", 10))
        layout.addWidget(category_label)
        
        self.book_category_input = QComboBox()
        self.book_category_input.setMinimumHeight(35)
        self.book_category_input.addItems([
            "Fiction",
            "Non-Fiction",
            "Science",
            "History",
            "Biography",
            "Mystery",
            "Romance",
            "Technology",
            "Self-Help",
            "Other"
        ])
        layout.addWidget(self.book_category_input)
        
        # Price
        price_label = QLabel("Price ($):")
        price_label.setFont(QFont("Arial", 10))
        layout.addWidget(price_label)
        
        self.book_price_input = QLineEdit()
        self.book_price_input.setPlaceholderText("Enter book price")
        self.book_price_input.setMinimumHeight(35)
        layout.addWidget(self.book_price_input)
        
        # Description
        description_label = QLabel("Description:")
        description_label.setFont(QFont("Arial", 10))
        layout.addWidget(description_label)
        
        self.book_description_input = QTextEdit()
        self.book_description_input.setPlaceholderText("Enter book description (optional)")
        self.book_description_input.setMinimumHeight(80)
        layout.addWidget(self.book_description_input)
        
        # Book Content
        content_label = QLabel("Book Content:")
        content_label.setFont(QFont("Arial", 10))
        layout.addWidget(content_label)
        
        self.book_content_input = QTextEdit()
        self.book_content_input.setPlaceholderText("Enter the book content here (users will read this)")
        self.book_content_input.setMinimumHeight(120)
        layout.addWidget(self.book_content_input)
        
        # Add button
        add_btn = QPushButton("Add Book")
        add_btn.setMinimumHeight(40)
        add_btn.setFont(QFont("Arial", 11, QFont.Bold))
        add_btn.clicked.connect(self.handle_add_book)
        layout.addWidget(add_btn)
        
        # Back button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setMinimumHeight(40)
        back_btn.setFont(QFont("Arial", 11))
        back_btn.clicked.connect(lambda: self.show_page(4))
        layout.addWidget(back_btn)
        
        page.setLayout(layout)
        return page
    
    def create_admin_view_books_page(self):
        """Create page for viewing books by category"""
        page = QWidget()
        main_layout = QHBoxLayout()
        
        # Left sidebar with categories
        left_layout = QVBoxLayout()
        left_frame = QFrame()
        left_frame.setMinimumWidth(200)
        left_frame.setMaximumWidth(250)
        
        cat_label = QLabel("Categories")
        cat_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(cat_label)
        
        self.category_list = QListWidget()
        self.category_list.itemClicked.connect(self.on_category_selected)
        left_layout.addWidget(self.category_list)
        
        left_frame.setLayout(left_layout)
        main_layout.addWidget(left_frame)
        
        # Right side with books
        right_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Books Library")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        # Books display
        self.books_display = QListWidget()
        self.books_display.itemClicked.connect(self.on_admin_book_selected)
        self.books_display.itemDoubleClicked.connect(self.handle_admin_view_book_info)
        right_layout.addWidget(self.books_display)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.clicked.connect(self.refresh_books_view)
        button_layout.addWidget(refresh_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.setMinimumHeight(35)
        delete_btn.clicked.connect(self.handle_delete_book)
        button_layout.addWidget(delete_btn)
        
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setMinimumHeight(35)
        back_btn.clicked.connect(lambda: self.show_page(4))
        button_layout.addWidget(back_btn)
        
        right_layout.addLayout(button_layout)
        
        right_frame = QFrame()
        right_frame.setLayout(right_layout)
        main_layout.addWidget(right_frame, 1)
        
        page.setLayout(main_layout)
        return page
    
    def create_admin_discount_page(self):
        """Create page for managing category discounts"""
        page = QWidget()
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Manage Category Discounts")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Categories label
        cat_label = QLabel("Select Category:")
        cat_label.setFont(QFont("Arial", 11, QFont.Bold))
        main_layout.addWidget(cat_label)
        
        # Category selection
        category_layout = QHBoxLayout()
        
        self.discount_category_combo = QComboBox()
        self.discount_category_combo.setMinimumHeight(35)
        self.discount_category_combo.addItems([
            "Fiction",
            "Non-Fiction",
            "Science",
            "History",
            "Biography",
            "Mystery",
            "Romance",
            "Technology",
            "Self-Help",
            "Other"
        ])
        category_layout.addWidget(self.discount_category_combo)
        main_layout.addLayout(category_layout)
        
        # Discount percentage
        discount_label = QLabel("Discount Percentage (0-100%):")
        discount_label.setFont(QFont("Arial", 11, QFont.Bold))
        main_layout.addWidget(discount_label)
        
        discount_input_layout = QHBoxLayout()
        
        self.discount_percentage_input = QLineEdit()
        self.discount_percentage_input.setPlaceholderText("Enter discount percentage (e.g., 10)")
        self.discount_percentage_input.setMinimumHeight(35)
        discount_input_layout.addWidget(self.discount_percentage_input)
        
        main_layout.addLayout(discount_input_layout)
        
        # Apply button
        apply_btn = QPushButton("Apply Discount")
        apply_btn.setMinimumHeight(40)
        apply_btn.setFont(QFont("Arial", 11, QFont.Bold))
        apply_btn.clicked.connect(self.handle_apply_discount)
        main_layout.addWidget(apply_btn)
        
        # Current discounts section
        current_label = QLabel("Current Category Discounts")
        current_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(current_label)
        
        # Discounts list
        self.discounts_list = QListWidget()
        self.discounts_list.setMinimumHeight(200)
        main_layout.addWidget(self.discounts_list)
        
        # Remove discount button
        remove_btn = QPushButton("Remove Selected Discount")
        remove_btn.setMinimumHeight(40)
        remove_btn.setFont(QFont("Arial", 11))
        remove_btn.clicked.connect(self.handle_remove_discount)
        main_layout.addWidget(remove_btn)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setFont(QFont("Arial", 11))
        refresh_btn.clicked.connect(self.refresh_discounts_view)
        main_layout.addWidget(refresh_btn)
        
        # Back button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setMinimumHeight(40)
        back_btn.setFont(QFont("Arial", 11))
        back_btn.clicked.connect(lambda: self.show_page(4))
        main_layout.addWidget(back_btn)
        
        page.setLayout(main_layout)
        return page
    
    def create_admin_user_management_page(self):
        """Create page for managing users (ban/unban)"""
        page = QWidget()
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("User Management")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Description
        desc_label = QLabel("Select users to ban or unban them:")
        desc_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(desc_label)
        
        # Users list
        self.users_list = QListWidget()
        self.users_list.setMinimumHeight(300)
        main_layout.addWidget(self.users_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Ban button
        ban_btn = QPushButton("Ban Selected User")
        ban_btn.setMinimumHeight(40)
        ban_btn.setFont(QFont("Arial", 11))
        ban_btn.clicked.connect(self.handle_ban_user)
        button_layout.addWidget(ban_btn)
        
        # Unban button
        unban_btn = QPushButton("Unban Selected User")
        unban_btn.setMinimumHeight(40)
        unban_btn.setFont(QFont("Arial", 11))
        unban_btn.clicked.connect(self.handle_unban_user)
        button_layout.addWidget(unban_btn)
        
        main_layout.addLayout(button_layout)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Users List")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setFont(QFont("Arial", 11))
        refresh_btn.clicked.connect(self.refresh_users_view)
        main_layout.addWidget(refresh_btn)
        
        # Back button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setMinimumHeight(40)
        back_btn.setFont(QFont("Arial", 11))
        back_btn.clicked.connect(lambda: self.show_page(4))
        main_layout.addWidget(back_btn)
        
        page.setLayout(main_layout)
        return page
    
    def refresh_users_view(self):
        """Refresh the users list"""
        success, users = self.db.get_all_users()
        
        if success:
            self.users_list.clear()
            for user_id, username, email, is_banned, created_at in users:
                status = "(BANNED)" if is_banned else "(Active)"
                user_text = f"{username}\nEmail: {email}\nStatus: {status}"
                
                item = QListWidgetItem(user_text)
                item.setData(Qt.UserRole, user_id)
                
                # Color code banned users
                if is_banned:
                    item.setForeground(Qt.red)
                else:
                    item.setForeground(Qt.green)
                
                self.users_list.addItem(item)
        else:
            QMessageBox.critical(self, "Error", "Failed to load users")
    
    def handle_ban_user(self):
        """Handle banning a user"""
        selected = self.users_list.currentItem()
        
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a user to ban")
            return
        
        user_id = selected.data(Qt.UserRole)
        username = selected.text().split('\n')[0]
        
        # Confirm ban
        reply = QMessageBox.question(self, "Confirm Ban", 
                                     f"Are you sure you want to ban user '{username}'?\nThey will not be able to login.")
        if reply == QMessageBox.Yes:
            success, message = self.db.ban_user(user_id)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_users_view()
                # Notify the specific user (targeted)
                actor_id = self.current_user[0] if self.current_user else None
                actor_name = self.current_user[1] if self.current_user else 'Admin'
                note_msg = f"{actor_name} has banned your account. Contact admin for details."
                self.db.add_notification(actor_id, note_msg, broadcast=False, target_user_id=user_id)
            else:
                QMessageBox.critical(self, "Error", message)
    
    def handle_unban_user(self):
        """Handle unbanning a user"""
        selected = self.users_list.currentItem()
        
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a user to unban")
            return
        
        user_id = selected.data(Qt.UserRole)
        username = selected.text().split('\n')[0]
        
        # Confirm unban
        reply = QMessageBox.question(self, "Confirm Unban", 
                                     f"Are you sure you want to unban user '{username}'?\nThey will be able to login again.")
        if reply == QMessageBox.Yes:
            success, message = self.db.unban_user(user_id)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_users_view()
                # Notify the specific user (targeted)
                actor_id = self.current_user[0] if self.current_user else None
                actor_name = self.current_user[1] if self.current_user else 'Admin'
                note_msg = f"{actor_name} has unbanned your account. You can login now."
                self.db.add_notification(actor_id, note_msg, broadcast=False, target_user_id=user_id)
            else:
                QMessageBox.critical(self, "Error", message)
    
    def handle_apply_discount(self):
        """Handle applying discount to a category"""
        category = self.discount_category_combo.currentText()
        discount_text = self.discount_percentage_input.text().strip()
        
        # Validation
        if not discount_text:
            QMessageBox.warning(self, "Input Error", "Please enter a discount percentage")
            return
        
        try:
            discount = float(discount_text)
            if discount < 0 or discount > 100:
                QMessageBox.warning(self, "Discount Error", "Discount must be between 0 and 100")
                return
        except ValueError:
            QMessageBox.warning(self, "Discount Error", "Please enter a valid number")
            return
        
        # Apply discount
        success, message = self.db.set_category_discount(category, discount)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.discount_percentage_input.clear()
            self.refresh_discounts_view()
            # Notify users about discount change
            if self.current_user:
                admin_id = self.current_user[0]
                admin_name = self.current_user[1]
            else:
                admin_id = None
                admin_name = 'Admin'
            note_msg = f"{admin_name} set discount {discount}% for category {category}"
            self.db.add_notification(admin_id, note_msg, broadcast=True)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def refresh_discounts_view(self):
        """Refresh the discounts list"""
        success, discounts = self.db.get_category_discounts()
        
        if success:
            self.discounts_list.clear()
            for discount_id, category, discount_pct, updated_at in discounts:
                discount_text = f"{category}: {discount_pct}% OFF"
                item = QListWidgetItem(discount_text)
                item.setData(Qt.UserRole, category)
                self.discounts_list.addItem(item)
        else:
            QMessageBox.critical(self, "Error", "Failed to load discounts")
    
    def handle_remove_discount(self):
        """Handle removing a discount"""
        selected = self.discounts_list.currentItem()
        
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a discount to remove")
            return
        
        category = selected.data(Qt.UserRole)
        
        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Remove", 
                                     f"Are you sure you want to remove the discount for {category}?")
        if reply == QMessageBox.Yes:
            success, message = self.db.delete_category_discount(category)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_discounts_view()
                if self.current_user:
                    admin_id = self.current_user[0]
                    admin_name = self.current_user[1]
                else:
                    admin_id = None
                    admin_name = 'Admin'
                note_msg = f"{admin_name} removed discount for category {category}"
                self.db.add_notification(admin_id, note_msg, broadcast=True)
            else:
                QMessageBox.critical(self, "Error", message)
    
    def handle_add_book(self):
        """Handle adding a new book"""
        title = self.book_title_input.text().strip()
        author = self.book_author_input.text().strip()
        category = self.book_category_input.currentText()
        price_text = self.book_price_input.text().strip()
        description = self.book_description_input.toPlainText().strip()
        content = self.book_content_input.toPlainText().strip()
        
        # Validation
        if not title or not author:
            QMessageBox.warning(self, "Input Error", "Title and Author are required")
            return
        
        # Validate price
        try:
            price = float(price_text) if price_text else 0.0
            if price < 0:
                QMessageBox.warning(self, "Price Error", "Price cannot be negative")
                return
        except ValueError:
            QMessageBox.warning(self, "Price Error", "Please enter a valid price")
            return
        
        # Add book to database
        success, message = self.db.add_book(title, author, category, price, description, content)
        
        if success:
            QMessageBox.information(self, "Success", message)
            # Clear fields
            self.book_title_input.clear()
            self.book_author_input.clear()
            self.book_price_input.clear()
            self.book_description_input.clear()
            self.book_content_input.clear()
            # Notify users about new book
            if self.current_user:
                admin_id = self.current_user[0]
                admin_name = self.current_user[1]
            else:
                admin_id = None
                admin_name = 'Admin'
            note_msg = f"{admin_name} added a new book: '{title}' in {category}"
            self.db.add_notification(admin_id, note_msg, broadcast=True)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def refresh_books_view(self):
        """Refresh the books view with latest data"""
        success, books_by_category = self.db.get_books_by_category()
        
        if success:
            # Clear and populate categories
            self.category_list.clear()
            for category in sorted(books_by_category.keys()):
                item = QListWidgetItem(f"{category} ({len(books_by_category[category])})")
                item.setData(Qt.UserRole, category)
                self.category_list.addItem(item)
            
            # Clear books display
            self.books_display.clear()
            
            # Store books data
            self.books_data = books_by_category
        else:
            QMessageBox.critical(self, "Error", books_by_category)
    
    def on_category_selected(self, item):
        """Handle category selection"""
        category = item.data(Qt.UserRole)
        
        # Display books for selected category
        self.books_display.clear()
        
        if hasattr(self, 'books_data') and category in self.books_data:
            # Get discount for this category
            success, discount = self.db.get_category_discount(category)
            
            for book in self.books_data[category]:
                book_id, title, author, price, description = book
                
                # Calculate discounted price if discount exists
                if success and discount > 0:
                    discounted_price = price * (1 - discount / 100)
                    book_text = f"{title}\nby {author}\nOriginal Price: ${price:.2f}\nDiscount: {discount}%\nFinal Price: ${discounted_price:.2f}"
                else:
                    book_text = f"{title}\nby {author}\nPrice: ${price:.2f}"
                
                if description:
                    book_text += f"\n{description}"
                
                list_item = QListWidgetItem(book_text)
                list_item.setData(Qt.UserRole, book_id)
                self.books_display.addItem(list_item)
    
    def handle_delete_book(self):
        """Handle deleting a selected book"""
        selected = self.books_display.currentItem()
        
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a book to delete")
            return
        
        book_id = selected.data(Qt.UserRole)
        
        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this book?")
        if reply == QMessageBox.Yes:
            # get title for notification
            gsucc, book = self.db.get_book_by_id(book_id)
            book_title = book[1] if gsucc and book else 'a book'

            success, message = self.db.delete_book(book_id)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_books_view()
                if self.current_user:
                    admin_id = self.current_user[0]
                    admin_name = self.current_user[1]
                else:
                    admin_id = None
                    admin_name = 'Admin'
                note_msg = f"{admin_name} deleted the book: '{book_title}'"
                self.db.add_notification(admin_id, note_msg, broadcast=True)
            else:
                QMessageBox.critical(self, "Error", message)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()
        
        # Validation
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return
        
        # Check if user is banned
        if self.db.is_user_banned(username):
            QMessageBox.critical(self, "Login Failed", "Your account has been banned. Please contact administrator.")
            return
        
        # Attempt login
        success, result = self.db.login_user(username, password)
        
        if success:
            user_id, username, email, role = result
            self.current_user = (user_id, username, email)
            self.user_role = role
            
            # Route to appropriate dashboard based on role
            if role == 'admin':
                self.show_page(4)  # Admin dashboard
            else:
                self.show_page(2)  # User dashboard
            
            self.update_dashboard()
            # Clear fields
            self.login_username.clear()
            self.login_password.clear()
        else:
            QMessageBox.critical(self, "Login Failed", result)
    
    def handle_signup(self):
        """Handle signup button click"""
        username = self.signup_username.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text().strip()
        confirm_password = self.signup_confirm_password.text().strip()
        
        # Validation
        if not username or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return
        
        if len(username) < 3 or len(username) > 20:
            QMessageBox.warning(self, "Username Error", "Username must be 3-20 characters")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Password Error", "Password must be at least 6 characters")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Password Error", "Passwords do not match")
            return
        
        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Email Error", "Please enter a valid email")
            return
        
        # Attempt registration
        success, message = self.db.register_user(username, email, password)
        
        if success:
            QMessageBox.information(self, "Success", message + "\nPlease login with your new account")
            # Clear fields and switch to login
            self.signup_username.clear()
            self.signup_email.clear()
            self.signup_password.clear()
            self.signup_confirm_password.clear()
            self.show_page(0)
        else:
            QMessageBox.critical(self, "Registration Failed", message)
    
    def update_dashboard(self):
        """Update dashboard with user information"""
        if self.current_user:
            user_id, username, email = self.current_user
            
            if self.user_role == 'admin':
                self.admin_welcome_label.setText(f"Welcome, Admin {username}!")
                self.admin_info_label.setText(f"Email: {email}\nID: {user_id}\nRole: Administrator")
            else:
                self.welcome_label.setText(f"Welcome, {username}!")
                self.user_info_label.setText(f"Email: {email}\nID: {user_id}")
                # Update notifications count on dashboard
                ok, notes = self.db.get_notifications_for_user(user_id)
                if ok and isinstance(notes, list):
                    count = len(notes)
                    try:
                        self.notifications_btn.setText(f"Notifications ({count})")
                    except Exception:
                        pass
    
    def handle_logout(self):
        """Handle logout"""
        self.current_user = None
        self.user_role = None
        self.show_page(0)
    
    def show_page(self, index):
        """Switch to specified page"""
        self.stacked_widget.setCurrentIndex(index)
    
    def show_users_management(self):
        """Show users management page"""
        self.refresh_users_view()
        self.show_page(8)
    
    def show_user_books_view(self):
        """Show user books view and load data"""
        self.refresh_user_books_view()
        self.show_page(3)
    
    def refresh_user_books_view(self):
        """Refresh the user books view with latest data"""
        success, books_by_category = self.db.get_books_by_category()
        
        if success:
            # Clear and populate categories
            self.user_category_list.clear()
            for category in sorted(books_by_category.keys()):
                item = QListWidgetItem(f"{category} ({len(books_by_category[category])})")
                item.setData(Qt.UserRole, category)
                self.user_category_list.addItem(item)
            
            # Clear books display
            self.user_books_display.clear()
            
            # Store books data
            self.user_books_data = books_by_category
        else:
            QMessageBox.critical(self, "Error", books_by_category)
    
    def on_user_category_selected(self, item):
        """Handle category selection for user"""
        category = item.data(Qt.UserRole)
        
        # Clear search when selecting category
        self.search_input.clear()
        
        # Display books for selected category
        self.user_books_display.clear()
        
        if hasattr(self, 'user_books_data') and category in self.user_books_data:
            # Get discount for this category
            success, discount = self.db.get_category_discount(category)
            
            for book in self.user_books_data[category]:
                book_id, title, author, price, description = book
                
                # Calculate discounted price if discount exists
                if success and discount > 0:
                    discounted_price = price * (1 - discount / 100)
                    book_text = f"{title}\nby {author}\nOriginal Price: ${price:.2f}\nDiscount: {discount}%\nFinal Price: ${discounted_price:.2f}"
                else:
                    book_text = f"{title}\nby {author}\nPrice: ${price:.2f}"
                
                if description:
                    book_text += f"\n{description}"
                
                list_item = QListWidgetItem(book_text)
                list_item.setData(Qt.UserRole, book_id)
                self.user_books_display.addItem(list_item)
    
    def handle_search_books(self):
        """Handle searching for books"""
        search_query = self.search_input.text().strip()
        
        if not search_query:
            QMessageBox.warning(self, "Search Error", "Please enter a search term")
            return
        
        success, results = self.db.search_books(search_query)
        
        if not success:
            QMessageBox.critical(self, "Error", results)
            return
        
        # Clear and display search results
        self.user_books_display.clear()
        self.user_category_list.clearSelection()
        
        if not results:
            QMessageBox.information(self, "Search Results", "No books found matching your search")
            return
        
        # Display search results
        for book in results:
            book_id, title, author, category, price, description = book
            
            # Get discount for this category
            success, discount = self.db.get_category_discount(category)
            
            # Calculate discounted price if discount exists
            if success and discount > 0:
                discounted_price = price * (1 - discount / 100)
                book_text = f"{title}\nby {author}\nCategory: {category}\nOriginal Price: ${price:.2f}\nDiscount: {discount}%\nFinal Price: ${discounted_price:.2f}"
            else:
                book_text = f"{title}\nby {author}\nCategory: {category}\nPrice: ${price:.2f}"
            
            if description:
                book_text += f"\n{description}"
            
            list_item = QListWidgetItem(book_text)
            list_item.setData(Qt.UserRole, book_id)
            self.user_books_display.addItem(list_item)
    
    def clear_search(self):
        """Clear search and show all books again"""
        self.search_input.clear()
        self.user_category_list.clearSelection()
        self.user_books_display.clear()
        self.refresh_user_books_view()
    
    def show_admin_books_view(self):
        """Show admin books view and load data"""
        self.refresh_books_view()
        self.show_page(6)
    
    def show_discount_management(self):
        """Show discount management page"""
        self.refresh_discounts_view()
        self.show_page(7)
    
    def on_user_book_selected(self, item):
        """Handle book selection in user books view"""
        # Show buy button when a book is selected
        self.buy_book_btn.setVisible(True)
        self.selected_book_item = item

        # Also show view info button
        self.view_info_btn.setVisible(True)
    
    def handle_buy_book(self):
        """Handle purchasing a selected book"""
        if not hasattr(self, 'selected_book_item') or self.selected_book_item is None:
            QMessageBox.warning(self, "Error", "Please select a book first")
            return
        
        book_id = self.selected_book_item.data(Qt.UserRole)
        user_id = self.current_user[0]
        
        # Call database to purchase the book
        success, message = self.db.purchase_book(user_id, book_id)
        
        if success:
            QMessageBox.information(self, "Purchase Successful", message)
            self.buy_book_btn.setVisible(False)
            self.user_books_display.clearSelection()
        else:
            QMessageBox.warning(self, "Purchase Failed", message)

    def on_admin_book_selected(self, item):
        """Handle admin selecting a book in admin view"""
        # Admin can view book info (including reviews)
        self.selected_admin_book_item = item

    def handle_admin_view_book_info(self, item):
        """Open book info dialog for admin when double-clicked"""
        book_id = item.data(Qt.UserRole)
        self.show_book_info_dialog(book_id)

    def handle_view_book_info(self):
        """Open a dialog showing book details and reviews; allow adding a review"""
        if not hasattr(self, 'selected_book_item') or self.selected_book_item is None:
            QMessageBox.warning(self, "Error", "Please select a book first")
            return

        book_id = self.selected_book_item.data(Qt.UserRole)
        self.show_book_info_dialog(book_id)

    def show_book_info_dialog(self, book_id):
        """Display a dialog with book details and its reviews; allow user reviews"""
        # Fetch book details
        success, book = self.db.get_book_by_id(book_id)
        if not success:
            QMessageBox.critical(self, "Error", book)
            return

        # Unpack book info
        _id, title, author, category, price, description, content = book

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Book Info - {title}")
        dialog.setMinimumSize(QSize(500, 400))

        layout = QVBoxLayout()

        header = QLabel(f"{title}\nby {author}\nCategory: {category}\nPrice: ${price:.2f}")
        header.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(header)

        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        # Reviews section
        reviews_label = QLabel("Reviews:")
        reviews_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(reviews_label)

        reviews_area = QScrollArea()
        reviews_area.setWidgetResizable(True)
        reviews_container = QWidget()
        reviews_layout = QVBoxLayout()

        # Load reviews
        r_success, reviews = self.db.get_reviews_for_book(book_id)
        if not r_success:
            reviews_layout.addWidget(QLabel("Failed to load reviews"))
        else:
            if not reviews:
                reviews_layout.addWidget(QLabel("No reviews yet. Be the first to review!"))
            else:
                for rev_id, user_id, username, rating, review_text, created_at in reviews:
                    rev_widget = QLabel(f"{username} ({created_at}):\n{review_text}")
                    rev_widget.setWordWrap(True)
                    reviews_layout.addWidget(rev_widget)

        reviews_container.setLayout(reviews_layout)
        reviews_area.setWidget(reviews_container)
        layout.addWidget(reviews_area, 1)

        # If logged in, allow adding a review
        if self.current_user:
            add_label = QLabel("Add Your Review:")
            add_label.setFont(QFont("Arial", 11, QFont.Bold))
            layout.addWidget(add_label)

            self.new_review_text = QTextEdit()
            self.new_review_text.setPlaceholderText("Write your review here...")
            self.new_review_text.setMinimumHeight(80)
            layout.addWidget(self.new_review_text)

            submit_btn = QPushButton("Submit Review")
            submit_btn.setMinimumHeight(35)

            def submit_review():
                text = self.new_review_text.toPlainText().strip()
                if not text:
                    QMessageBox.warning(dialog, "Input Error", "Please write a review before submitting")
                    return

                user_id = self.current_user[0]
                ok, msg = self.db.add_review(user_id, book_id, text)
                if ok:
                    QMessageBox.information(dialog, "Success", msg)
                    # refresh dialog: close and reopen to show new review
                    dialog.accept()
                    self.show_book_info_dialog(book_id)
                else:
                    QMessageBox.critical(dialog, "Error", msg)

            submit_btn.clicked.connect(submit_review)
            layout.addWidget(submit_btn)

        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(35)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.setLayout(layout)
        dialog.exec()
    
    def show_user_purchases(self):
        """Show user's purchase history"""
        self.refresh_purchases_view()
        self.show_page(9)

    def show_notifications(self):
        """Show notifications dialog for current user"""
        if not self.current_user:
            QMessageBox.warning(self, "Not Logged In", "Please login to view notifications")
            return

        user_id = self.current_user[0]
        ok, notes = self.db.get_notifications_for_user(user_id)

        dialog = QDialog(self)
        dialog.setWindowTitle("Notifications")
        dialog.setMinimumSize(QSize(500, 400))
        layout = QVBoxLayout()

        if not ok:
            layout.addWidget(QLabel("Failed to load notifications"))
        else:
            if not notes:
                layout.addWidget(QLabel("No notifications"))
            else:
                for nid, actor_id, actor_username, message, is_broadcast, target_user_id, created_at in notes:
                    who = actor_username if actor_username else 'Admin'
                    item = QLabel(f"{created_at} - {who}: {message}")
                    item.setWordWrap(True)
                    layout.addWidget(item)

        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(35)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.setLayout(layout)
        dialog.exec()
    
    def refresh_purchases_view(self):
        """Refresh user's purchases display"""
        user_id = self.current_user[0]
        success, purchases = self.db.get_user_purchases(user_id)
        
        self.user_purchases_display.clear()
        self.user_purchases_data = {}  # Store book_id mapping
        
        if not success:
            QMessageBox.critical(self, "Error", purchases)
            return
        
        if not purchases:
            no_purchases_item = QListWidgetItem("You have not purchased any books yet")
            no_purchases_item.setFont(QFont("Arial", 11))
            self.user_purchases_display.addItem(no_purchases_item)
            return
        
        for purchase in purchases:
            purchase_id, title, author, category, orig_price, discount_amount, final_price, purchase_date = purchase
            
            # Get book_id for this purchase
            cursor = self.db.db_path  # Need to get book_id, let's use a simpler approach
            
            purchase_text = f"{title}\nby {author}\nCategory: {category}\nOriginal Price: ${orig_price:.2f}\nDiscount: ${discount_amount:.2f}\nFinal Price: ${final_price:.2f}\nPurchased: {purchase_date}"
            
            list_item = QListWidgetItem(purchase_text)
            list_item.setData(Qt.UserRole, purchase_id)
            list_item.setFont(QFont("Arial", 10))
            self.user_purchases_data[purchase_id] = title  # Store for reference
            self.user_purchases_display.addItem(list_item)
        
        # Connect item selection to show read button
        self.user_purchases_display.itemClicked.connect(self.on_purchase_selected)
    
    def on_purchase_selected(self, item):
        """Handle purchase selection"""
        self.read_book_btn.setVisible(True)
        self.selected_purchase_item = item
    
    def handle_read_book(self):
        """Handle reading a purchased book"""
        if not hasattr(self, 'selected_purchase_item') or self.selected_purchase_item is None:
            QMessageBox.warning(self, "Error", "Please select a book first")
            return
        
        purchase_id = self.selected_purchase_item.data(Qt.UserRole)
        
        # Get book_id from purchase - we need to query the database
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT book_id FROM purchases WHERE id = ?', (purchase_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            QMessageBox.critical(self, "Error", "Could not find book")
            return
        
        book_id = result[0]
        
        # Get book content
        success, book_data = self.db.get_book_content(book_id)
        
        if not success:
            QMessageBox.critical(self, "Error", book_data)
            return
        
        title, author, content = book_data
        
        # Display book in reader
        self.reader_book_title.setText(title)
        self.reader_book_author.setText(f"by {author}")
        self.book_content_display.setText(content if content else "No content available for this book")
        
        self.show_page(10)  # Show book reader page
    
    def apply_stylesheet(self):
        """Apply stylesheet to the application"""
        stylesheet = """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLabel {
                color: #333333;
            }
        """
        self.setStyleSheet(stylesheet)


def main():
    app = QApplication(sys.argv)
    window = LoginSignupApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
