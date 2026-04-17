# 🚀 QUICK START GUIDE

## For Absolute Beginners - Step by Step

### ✅ Prerequisites Check

**1. Check if Python is installed:**
```bash
python --version
```
If not installed: Download from https://www.python.org/downloads/

**2. Check if MySQL is installed:**
```bash
mysql --version
```
If not installed: Download XAMPP from https://www.apachefriends.org/

---

## 🎯 FASTEST WAY TO RUN (5 Minutes)

### Step 1: Setup Database (2 minutes)

**If using XAMPP:**
1. Start XAMPP Control Panel
2. Start Apache and MySQL
3. Open phpMyAdmin: http://localhost/phpmyadmin
4. Click "New" to create database
5. Name it: `cafe_management`
6. Click "Import" tab
7. Choose file: `database.sql`
8. Click "Go"

**If using MySQL Command Line:**
```bash
mysql -u root -p
# Enter your password
CREATE DATABASE cafe_management;
USE cafe_management;
source C:/path/to/database.sql
# OR just copy-paste the SQL content
```

### Step 2: Install Python Packages (1 minute)

```bash
cd cafe_management
pip install Flask Flask-MySQLdb Werkzeug python-dotenv
```

**If mysqlclient fails on Windows:**
```bash
pip install pipwin
pipwin install mysqlclient
```

### Step 3: Configure Database (30 seconds)

Open `config.py` and update:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Your MySQL password (empty for XAMPP)
MYSQL_DB = 'cafe_management'
```

### Step 4: Run the Application (30 seconds)

```bash
python app.py
```

### Step 5: Open in Browser

Go to: **http://localhost:5000**

---

## 🔐 Login Credentials

**Admin:**
- Email: admin@cafe.com
- Password: admin123

**Customer:**
- Register a new account

---

## 🎨 What to Do First

### As Admin:
1. Login with admin credentials
2. Go to Admin Dashboard
3. Add some menu items
4. Check orders section

### As Customer:
1. Register new account
2. Browse menu
3. Add items to cart
4. Place an order
5. Book a table

---

## ⚡ Common Issues & Quick Fixes

### Issue 1: Can't connect to MySQL
```
Solution: Make sure MySQL is running in XAMPP or Services
```

### Issue 2: Module 'flask' not found
```bash
Solution: pip install -r requirements.txt
```

### Issue 3: mysqlclient won't install
```bash
Windows: Download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
Then: pip install downloaded_file.whl
```

### Issue 4: Port 5000 already in use
```python
Solution: In app.py, change the last line to:
app.run(debug=True, port=8000)
Then visit: http://localhost:8000
```

---

## 📱 Test the Features

### Customer Flow:
1. ✅ Register → Login
2. ✅ Browse Menu → Add to Cart
3. ✅ View Cart → Place Order
4. ✅ View Order History → See Invoice
5. ✅ Book a Table

### Admin Flow:
1. ✅ Login as admin
2. ✅ View Dashboard (statistics)
3. ✅ Add Menu Item
4. ✅ Update Order Status
5. ✅ Manage Bookings

---

## 🎯 Project Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Main application - all routes and logic |
| `config.py` | Settings and MySQL connection |
| `database.sql` | Database structure and sample data |
| `requirements.txt` | Python packages needed |
| `templates/` | All HTML pages |
| `static/css/` | Styling files |
| `static/js/` | JavaScript for interactions |

---

## 💡 Quick Customization Tips

### Change App Name:
In `templates/base.html`, find "Café Delight" and replace

### Change Colors:
In `static/css/style.css`, modify the color codes

### Add More Menu Items:
Login as admin → Manage Menu → Add Item

### Change Tax Rate:
In `config.py`, modify `TAX_RATE = 0.05` (5%)

---

## 🔄 Reset Everything

If you want to start fresh:

```bash
# 1. Drop and recreate database
mysql -u root -p
DROP DATABASE cafe_management;
CREATE DATABASE cafe_management;
USE cafe_management;
source database.sql;

# 2. Restart Flask
python app.py
```

---

## 📞 Still Having Issues?

1. Make sure MySQL is running
2. Check if database was created: `SHOW DATABASES;`
3. Verify tables exist: `USE cafe_management; SHOW TABLES;`
4. Check Python version: `python --version` (should be 3.8+)
5. Reinstall packages: `pip install -r requirements.txt --force-reinstall`

---

## ✅ You're All Set!

The application should now be running at **http://localhost:5000**

Enjoy your Café Management System! 🎉

---

**Need More Help?**
Read the detailed `README.md` for complete documentation.
