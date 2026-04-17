from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import razorpay
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# MySQL
mysql = MySQL(app)

# Razorpay client ✅ (correct place)
client = razorpay.Client(auth=("rzp_test_Sd1rntkzstOsGE", "ofLAWWPbNWup24t2Ovay7FVw"))

# Helper
def is_logged_in():
    return 'user_id' in session

# Helper function to check if user is admin
def is_admin():
    return session.get('is_admin', False)

# Helper function to get cart count
def get_cart_count():
    return len(session.get('cart', []))

# Context processor to make variables available in all templates
@app.context_processor
def inject_globals():
    return {
        'is_logged_in': is_logged_in(),
        'is_admin': is_admin(),
        'cart_count': get_cart_count(),
        'user_name': session.get('user_name', '')
    }

# ============== HOME ROUTE ==============
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu_items LIMIT 5")
    featured_items = cur.fetchall()   # this is LIST
    cur.close()

    return render_template('index.html', featured_items=featured_items)

# ============== AUTHENTICATION ROUTES ==============
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                       (name, email, phone, hashed_password))
            mysql.connection.commit()
            cur.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['is_admin'] = user['is_admin']
            
            flash(f'Welcome back, {user["name"]}!', 'success')
            
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ============== MENU ROUTES ==============
@app.route('/menu')
def menu():
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    cur = mysql.connection.cursor()
    
    # Get all categories
    cur.execute("SELECT * FROM categories ORDER BY name")
    categories = cur.fetchall()
    
    # Build query based on filters
    query = """
        SELECT m.*, c.name as category_name 
        FROM menu_items m 
        LEFT JOIN categories c ON m.category_id = c.id 
        WHERE m.is_available = TRUE
    """
    params = []
    
    if category_filter:
        query += " AND c.name = %s"
        params.append(category_filter)
    
    if search_query:
        query += " AND m.name LIKE %s"
        params.append(f'%{search_query}%')
    
    query += " ORDER BY m.name"
    
    cur.execute(query, params)
    menu_items = cur.fetchall()
    cur.close()
    
    return render_template('menu.html', menu_items=menu_items, categories=categories, 
                         selected_category=category_filter, search_query=search_query)

# ============== CART ROUTES ==============
@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(item_id)

    flash('Item added to cart!', 'success')
    return redirect(url_for('menu'))
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = []

    # Add item to cart (list)
    session['cart'].append(item_id)

    flash('Item added to cart!', 'success')
    return redirect(url_for('menu'))
@app.route('/cart')
def cart():
    if not is_logged_in():
        flash('Please login to view your cart.', 'warning')
        return redirect(url_for('login'))
    
    cart_ids = session.get('cart', [])   # list of item IDs
    cart_items = []
    subtotal = 0

    cur = mysql.connection.cursor()

    for item_id in cart_ids:
        cur.execute("SELECT * FROM menu_items WHERE id=%s", (item_id,))
        item = cur.fetchone()

        if item:
            item['quantity'] = 1
            item['subtotal'] = item['price'] * 1
            subtotal += float(item['price'])
            cart_items.append(item)

    tax = subtotal * app.config['TAX_RATE']
    total = subtotal + tax
    
    # Get available tables
    cur.execute("SELECT * FROM tables WHERE status = 'available' ORDER BY table_number")
    tables = cur.fetchall()
    cur.close()

    return render_template('cart.html',
                           cart_items=cart_items,
                           subtotal=subtotal,
                           tax=tax,
                           total=total,
                           tables=tables)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    quantity = int(request.form.get('quantity', 1))
    item_key = str(item_id)
    
    if 'cart' in session and item_key in session['cart']:
        if quantity > 0:
            session['cart'][item_key]['quantity'] = quantity
        else:
            del session['cart'][item_key]
        session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    if 'cart' in session and item_id in session['cart']:
        session['cart'].remove(item_id)

    flash('Item removed!', 'success')
    return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared.', 'info')
    return redirect(url_for('cart'))

# ============== ORDER ROUTES ==============
@app.route('/place_order', methods=['POST'])
def place_order():
    if not is_logged_in():
        return redirect(url_for('login'))

    try:
        # ✅ ALWAYS FIRST
        cur = mysql.connection.cursor()

        cart_ids = session.get('cart', [])

        if not cart_ids:
            flash("Cart is empty", "warning")
            return redirect(url_for('cart'))

        order_type = request.form.get('order_type')
        table_id = request.form.get('table_id') or None

        # Calculate total
        subtotal = 0
        unique_ids = set(cart_ids)

        for item_id in unique_ids:
            cur.execute("SELECT price FROM menu_items WHERE id=%s", (item_id,))
            item = cur.fetchone()

            if item:
                qty = cart_ids.count(item_id)
                subtotal += float(item['price']) * qty

        tax = subtotal * 0.05
        discount = 0
        final_amount = subtotal + tax

        # Insert order
        cur.execute("""
            INSERT INTO orders (user_id, table_id, order_type, total_price, tax, discount, final_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session['user_id'], table_id, order_type, subtotal, tax, discount, final_amount))

        order_id = cur.lastrowid

        # Insert items
        for item_id in unique_ids:
            cur.execute("SELECT * FROM menu_items WHERE id=%s", (item_id,))
            item = cur.fetchone()

            if item:
                qty = cart_ids.count(item_id)
                price = float(item['price'])

                cur.execute("""
                    INSERT INTO order_items (order_id, menu_item_id, quantity, price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, item_id, qty, price, price * qty))

        # Update table
        if table_id:
            cur.execute("UPDATE tables SET status='occupied' WHERE id=%s", (table_id,))

        mysql.connection.commit()
        cur.close()

        # Clear cart
        session['cart'] = []

        flash("Order placed successfully!", "success")
        return redirect(url_for('invoice', order_id=order_id))

    except Exception as e:
        print("ERROR:", e)   # 🔥 debug
        flash("Error placing order", "danger")
        return redirect(url_for('cart'))

@app.route('/order_history')
def order_history():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT o.*, t.table_number
        FROM orders o
        LEFT JOIN tables t ON o.table_id = t.id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC
    """, [session['user_id']])
    orders = cur.fetchall()
    cur.close()
    
    return render_template('order_history.html', orders=orders)

@app.route('/invoice/<int:order_id>')
def invoice(order_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    
    # Get order details
    cur.execute("""
        SELECT o.*, u.name as customer_name, u.email, u.phone, t.table_number
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN tables t ON o.table_id = t.id
        WHERE o.id = %s AND o.user_id = %s
    """, (order_id, session['user_id']))
    order = cur.fetchone()
    
    if not order:
        flash('Order not found!', 'danger')
        return redirect(url_for('order_history'))
    
    # Get order items
    cur.execute("""
        SELECT oi.*, m.name as item_name
        FROM order_items oi
        JOIN menu_items m ON oi.menu_item_id = m.id
        WHERE oi.order_id = %s
    """, [order_id])
    order_items = cur.fetchall()
    cur.close()
    
    return render_template('invoice.html', order=order, order_items=order_items)

# ============== BOOKING ROUTES ==============
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if not is_logged_in():
        flash('Please login to book a table.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        booking_date = request.form['booking_date']
        booking_time = request.form['booking_time']
        persons = int(request.form['persons'])
        special_request = request.form.get('special_request', '')
        
        try:
            cur = mysql.connection.cursor()
            
            # Find suitable available table
            cur.execute("""
                SELECT id FROM tables 
                WHERE status = 'available' AND capacity >= %s
                ORDER BY capacity ASC
                LIMIT 1
            """, [persons])
            table = cur.fetchone()
            
            if not table:
                flash('No tables available for the requested capacity.', 'warning')
                return redirect(url_for('booking'))
            
            # Create booking
            cur.execute("""
                INSERT INTO bookings (user_id, table_id, booking_date, booking_time, persons, special_request)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (session['user_id'], table['id'], booking_date, booking_time, persons, special_request))
            
            # Update table status
            cur.execute("UPDATE tables SET status = 'reserved' WHERE id = %s", [table['id']])
            
            mysql.connection.commit()
            cur.close()
            
            flash('Table booked successfully! Proceed to payment.', 'success')
            return redirect(url_for('checkout'))
        
        except Exception as e:
            flash('Error booking table. Please try again.', 'danger')
    
    # Get available tables for display
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tables WHERE status = 'available' ORDER BY capacity")
    tables = cur.fetchall()
    cur.close()
    
    from datetime import datetime

    return render_template('booking.html', tables=tables, now=datetime.now())

# ============== ADMIN ROUTES ==============
@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_logged_in() or not is_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    
    # Get statistics
    cur.execute("SELECT COUNT(*) as count FROM orders WHERE DATE(order_date) = CURDATE()")
    today_orders = cur.fetchone()['count']
    
    cur.execute("SELECT COALESCE(SUM(final_amount), 0) as revenue FROM orders WHERE DATE(order_date) = CURDATE() AND payment_status = 'paid'")
    today_revenue = cur.fetchone()['revenue']
    
    cur.execute("SELECT COUNT(*) as count FROM bookings WHERE status = 'pending'")
    pending_bookings = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = FALSE")
    total_customers = cur.fetchone()['count']
    
    # Recent orders
    cur.execute("""
        SELECT o.*, u.name as customer_name 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        ORDER BY o.order_date DESC 
        LIMIT 10
    """)
    recent_orders = cur.fetchall()
    
    cur.close()
    
    return render_template('admin/dashboard.html', 
                         today_orders=today_orders,
                         today_revenue=today_revenue,
                         pending_bookings=pending_bookings,
                         total_customers=total_customers,
                         recent_orders=recent_orders)

@app.route('/admin/menu', methods=['GET', 'POST'])
def admin_menu():
    if not is_logged_in() or not is_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form['name']
            category_id = request.form['category_id']
            description = request.form['description']
            price = request.form['price']
            image = request.form.get('image', 'default.jpg')
            
            cur.execute("""
                INSERT INTO menu_items (name, category_id, description, price, image)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, category_id, description, price, image))
            mysql.connection.commit()
            flash('Menu item added successfully!', 'success')
        
        elif action == 'update':
            item_id = request.form['item_id']
            name = request.form['name']
            category_id = request.form['category_id']
            description = request.form['description']
            price = request.form['price']
            is_available = request.form.get('is_available') == 'on'
            
            cur.execute("""
                UPDATE menu_items 
                SET name = %s, category_id = %s, description = %s, price = %s, is_available = %s
                WHERE id = %s
            """, (name, category_id, description, price, is_available, item_id))
            mysql.connection.commit()
            flash('Menu item updated successfully!', 'success')
        
        elif action == 'delete':
            item_id = request.form['item_id']
            cur.execute("DELETE FROM menu_items WHERE id = %s", [item_id])
            mysql.connection.commit()
            flash('Menu item deleted successfully!', 'success')
    
    # Get all menu items and categories
    cur.execute("""
        SELECT m.*, c.name as category_name 
        FROM menu_items m 
        LEFT JOIN categories c ON m.category_id = c.id 
        ORDER BY m.name
    """)
    menu_items = cur.fetchall()
    
    cur.execute("SELECT * FROM categories ORDER BY name")
    categories = cur.fetchall()
    
    cur.close()
    
    return render_template('admin/manage_menu.html', menu_items=menu_items, categories=categories)

@app.route('/admin/orders')
def admin_orders():
    if not is_logged_in() or not is_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT o.*, u.name as customer_name, t.table_number
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN tables t ON o.table_id = t.id
        ORDER BY o.order_date DESC
    """)
    orders = cur.fetchall()
    cur.close()
    
    return render_template('admin/manage_orders.html', orders=orders)

@app.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False})
    
    status = request.form.get('status')
    payment_status = request.form.get('payment_status')
    
    cur = mysql.connection.cursor()
    
    if status:
        cur.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
        
        # If order is completed, free up the table
        if status == 'completed':
            cur.execute("""
                UPDATE tables t
                JOIN orders o ON t.id = o.table_id
                SET t.status = 'available'
                WHERE o.id = %s
            """, [order_id])
    
    if payment_status:
        cur.execute("UPDATE orders SET payment_status = %s WHERE id = %s", (payment_status, order_id))
    
    mysql.connection.commit()
    cur.close()
    
    flash('Order updated successfully!', 'success')
    return redirect(url_for('admin_orders'))

@app.route('/admin/bookings')
def admin_bookings():
    if not is_logged_in() or not is_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.*, u.name as customer_name, u.phone, t.table_number
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        LEFT JOIN tables t ON b.table_id = t.id
        ORDER BY b.booking_date DESC, b.booking_time DESC
    """)
    bookings = cur.fetchall()
    cur.close()
    
    return render_template('admin/manage_bookings.html', bookings=bookings)

@app.route('/admin/update_booking_status/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False})
    
    status = request.form.get('status')
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE bookings SET status = %s WHERE id = %s", (status, booking_id))
    
    # If booking is cancelled or completed, free up the table
    if status in ['cancelled', 'completed']:
        cur.execute("""
            UPDATE tables t
            JOIN bookings b ON t.id = b.table_id
            SET t.status = 'available'
            WHERE b.id = %s
        """, [booking_id])
    
    mysql.connection.commit()
    cur.close()
    
    flash('Booking updated successfully!', 'success')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/users')
def admin_users():
    if not is_logged_in() or not is_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    
    return render_template('admin/manage_users.html', users=users)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cur = mysql.connection.cursor()
    total = 0

    for item_id in session.get('cart', []):
        cur.execute("SELECT * FROM menu_items WHERE id=%s", (item_id,))
        item = cur.fetchone()
        if item:
            total += float(item['price'])

    if total <= 0:
        total = 100

    # 👉 If user selects payment method
    if request.method == 'POST':
        payment_method = request.form['payment_method']

        if payment_method == 'cash':
            # Save order directly
            cur.execute("INSERT INTO orders(user_id, total_price, payment_status) VALUES (%s, %s, %s)",
                        (session['user_id'], total, 'Cash Pending'))
            mysql.connection.commit()

            return redirect(url_for('invoice', order_id=cur.lastrowid))

        elif payment_method == 'online':
            order = client.order.create({
                "amount": int(total * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            return render_template("payment.html", order=order, total=total)

    cur.close()
    return render_template("checkout.html", total=total)
@app.route('/success')
def success():
    cur = mysql.connection.cursor()

    total = 0
    for item_id in session.get('cart', []):
        cur.execute("SELECT price FROM menu_items WHERE id=%s", (item_id,))
        item = cur.fetchone()
        if item:
            total += float(item[0])

    # Save order with payment status
    cur.execute("""
 INSERT INTO orders(user_id, total_price, final_amount, payment_status)
 VALUES (%s, %s, %s, %s)
 """, (session['user_id'], total, total, 'Paid'))

    mysql.connection.commit()

    order_id = cur.lastrowid  # get last inserted order

    cur.close()

    session['cart'] = []

    # 👉 Redirect to invoice page
    return redirect(url_for('invoice', order_id=order_id))
if __name__ == '__main__':
    app.run(debug=True)
