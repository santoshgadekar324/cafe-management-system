# 🍕 Café Management System

A complete, production-ready Café Management Web Application built with Python Flask, MySQL, Bootstrap, and JavaScript.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Default Credentials](#default-credentials)
- [Project Structure](#project-structure)
- [Features Breakdown](#features-breakdown)
- [Screenshots](#screenshots)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Customer Features
- ✅ User Registration & Login (with password hashing)
- ✅ Browse menu items with categories
- ✅ Search and filter menu items
- ✅ Add items to cart
- ✅ Place orders (Dine-in / Takeaway)
- ✅ Table booking system
- ✅ View order history
- ✅ Generate and print invoices
- ✅ Responsive design for mobile and desktop

### Admin Features
- ✅ Admin dashboard with statistics
- ✅ Manage menu items (Add/Edit/Delete)
- ✅ Manage orders and update status
- ✅ Manage table bookings
- ✅ View all users
- ✅ Real-time order tracking
- ✅ Revenue tracking

### Technical Features
- ✅ Session-based authentication
- ✅ Password hashing with Werkzeug
- ✅ Input validation and sanitization
- ✅ Flash messages for user feedback
- ✅ AJAX cart functionality
- ✅ Print-friendly invoices
- ✅ Tax calculation (5% GST)
- ✅ Table availability management

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **MySQL** - Database
- **Flask-MySQLdb** - MySQL connector
- **Werkzeug** - Password hashing

### Frontend
- **HTML5**
- **CSS3**
- **Bootstrap 5.3** - UI framework
- **JavaScript** - Client-side logic
- **jQuery** - AJAX requests
- **Font Awesome** - Icons
- **Google Fonts** - Typography

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **MySQL Server**
   ```bash
   mysql --version
   ```

3. **pip (Python package manager)**
   ```bash
   pip --version
   ```

## 🚀 Installation

### Step 1: Clone or Download the Project

Download the project files to your local machine.

### Step 2: Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd cafe_management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues with `mysqlclient`, install these first:

**On Windows:**
Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

**On macOS:**
```bash
brew install mysql
```

## 🗄️ Database Setup

### Step 1: Start MySQL Server

Make sure your MySQL server is running.

**Windows:**
- Start from Services or XAMPP/WAMP

**macOS/Linux:**
```bash
sudo service mysql start
# or
sudo systemctl start mysql
```

### Step 2: Create Database and Tables

**Option 1: Using MySQL Command Line**

```bash
# Login to MySQL
mysql -u root -p

# Run the SQL file
source /path/to/cafe_management/database.sql
```

**Option 2: Using phpMyAdmin**

1. Open phpMyAdmin
2. Create a new database named `cafe_management`
3. Import the `database.sql` file

**Option 3: Manual Execution**

```bash
# Login to MySQL
mysql -u root -p

# Copy and paste the contents of database.sql
```

### Step 3: Configure Database Connection

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your MySQL credentials:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DB=cafe_management
   ```

**OR** edit `config.py` directly:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'cafe_management'
```

## ▶️ Running the Application

### Step 1: Activate Virtual Environment (if not already active)

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 2: Run Flask Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 🔐 Default Credentials

### Admin Account
- **Email:** admin@cafe.com
- **Password:** admin123

### Create Customer Account
Register a new account from the registration page.

## 📁 Project Structure

```
cafe_management/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.sql                # Database schema and sample data
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── menu.html              # Menu listing page
│   ├── cart.html              # Shopping cart
│   ├── booking.html           # Table booking
│   ├── order_history.html     # Order history
│   ├── invoice.html           # Invoice/Bill page
│   └── admin/                 # Admin templates
│       ├── dashboard.html     # Admin dashboard
│       ├── manage_menu.html   # Menu management
│       ├── manage_orders.html # Order management
│       ├── manage_bookings.html # Booking management
│       └── manage_users.html  # User management
│
└── static/                     # Static files
    ├── css/
    │   └── style.css          # Custom CSS
    ├── js/
    │   └── script.js          # Custom JavaScript
    └── images/                # Image uploads
```

## 🎯 Features Breakdown

### 1. Authentication System
- Secure password hashing using Werkzeug
- Session-based login
- Role-based access control (Admin/Customer)
- Protected routes

### 2. Menu Management
- Category-wise organization
- Search functionality
- Filter by category
- Admin can add/edit/delete items
- Availability toggle

### 3. Shopping Cart
- Add/remove items
- Update quantities
- Real-time price calculation
- Tax computation
- Session-based storage

### 4. Order System
- Dine-in and takeaway options
- Table selection for dine-in
- Order status tracking (Pending → Preparing → Ready → Completed)
- Payment status management
- Order history

### 5. Table Booking
- Date and time selection
- Number of persons
- Automatic table assignment
- Special requests
- Booking status management

### 6. Billing & Invoice
- Detailed invoice generation
- Item-wise breakdown
- Tax calculation
- Discount support
- Print functionality

### 7. Admin Dashboard
- Today's orders count
- Revenue tracking
- Pending bookings
- Customer statistics
- Recent orders view

## 🌐 API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Menu
- `GET /menu` - View menu (with search & filter)
- `POST /add_to_cart/<item_id>` - Add item to cart

### Cart & Orders
- `GET /cart` - View shopping cart
- `POST /update_cart/<item_id>` - Update cart quantity
- `GET /remove_from_cart/<item_id>` - Remove item from cart
- `POST /place_order` - Place new order
- `GET /order_history` - View order history
- `GET /invoice/<order_id>` - View invoice

### Booking
- `GET/POST /booking` - Table booking

### Admin Routes (Protected)
- `GET /admin/dashboard` - Admin dashboard
- `GET/POST /admin/menu` - Manage menu items
- `GET /admin/orders` - View all orders
- `POST /admin/update_order_status/<order_id>` - Update order status
- `GET /admin/bookings` - View all bookings
- `POST /admin/update_booking_status/<booking_id>` - Update booking status
- `GET /admin/users` - View all users

## 🔍 Troubleshooting

### MySQL Connection Error
```
Error: Can't connect to MySQL server
```
**Solution:**
1. Ensure MySQL server is running
2. Check credentials in `config.py`
3. Verify database exists: `SHOW DATABASES;`

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### mysqlclient Installation Error
**Windows:**
Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

**Linux:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

### Port 5000 Already in Use
**Solution:**
Change port in `app.py`:
```python
app.run(debug=True, port=8000)
```

### Database Tables Not Created
**Solution:**
```bash
mysql -u root -p cafe_management < database.sql
```

### Static Files Not Loading
**Solution:**
1. Check `static` folder exists
2. Clear browser cache
3. Restart Flask server

## 📸 Usage Guide

### For Customers:
1. **Register** - Create a new account
2. **Browse Menu** - View available items
3. **Add to Cart** - Select items and quantities
4. **Place Order** - Choose dine-in or takeaway
5. **Book Table** - Reserve a table for future visit
6. **View Orders** - Check order history and invoices

### For Admin:
1. **Login** with admin credentials
2. **Dashboard** - View statistics
3. **Manage Menu** - Add/edit/delete items
4. **Process Orders** - Update order status
5. **Handle Bookings** - Confirm/cancel bookings
6. **View Users** - Monitor customer accounts

## 🔒 Security Features

- Password hashing with Werkzeug
- SQL injection prevention (parameterized queries)
- XSS protection (Flask auto-escaping)
- CSRF protection (can be enhanced with Flask-WTF)
- Session security
- Input validation

## 🚀 Deployment Recommendations

### For Production:
1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (Gunicorn/uWSGI)
3. Set up HTTPS with SSL certificate
4. Use environment variables for sensitive data
5. Enable database backups
6. Implement rate limiting
7. Add CSRF protection with Flask-WTF
8. Set up logging

### Deployment Platforms:
- **Heroku** (with ClearDB MySQL add-on)
- **PythonAnywhere**
- **AWS EC2** with RDS
- **DigitalOcean** Droplet
- **Google Cloud Platform**

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Developer Notes

### To Add New Features:
1. Create route in `app.py`
2. Create template in `templates/`
3. Add styling in `static/css/style.css`
4. Add client-side logic in `static/js/script.js`

### Database Modifications:
1. Update `database.sql`
2. Run migration on MySQL
3. Update models/queries in `app.py`

## 🆘 Support

If you encounter any issues:
1. Check the Troubleshooting section
2. Verify all prerequisites are installed
3. Ensure MySQL server is running
4. Check Flask console for error messages

## ✅ Testing Checklist

- [ ] User registration works
- [ ] User login works
- [ ] Admin login works
- [ ] Menu displays correctly
- [ ] Add to cart works
- [ ] Cart updates properly
- [ ] Order placement succeeds
- [ ] Invoice generates correctly
- [ ] Table booking works
- [ ] Admin can manage menu
- [ ] Admin can update order status
- [ ] Admin can manage bookings

## 🎉 Congratulations!

You now have a fully functional Café Management System. Enjoy exploring and customizing it!

---

**Built with ❤️ using Flask, MySQL, and Bootstrap**
