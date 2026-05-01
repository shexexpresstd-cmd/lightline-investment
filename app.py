"""
Lightline Investment Group - Multi-Site Flask Application
Parent Company + 5 Subsidiary Websites
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3
import os
from contextlib import contextmanager

from blueprints.main_bp import main_bp
from blueprints.engineering_bp import engineering_bp
from blueprints.logistics_bp import logistics_bp
from blueprints.capital_bp import capital_bp
from blueprints.research_bp import research_bp
from blueprints.cfe_bp import cfe_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lightline_secret_key_2024'
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'lightline_investment.db')

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(engineering_bp)
app.register_blueprint(logistics_bp)
app.register_blueprint(capital_bp)
app.register_blueprint(research_bp)
app.register_blueprint(cfe_bp)

# ============================================================
# DATABASE SETUP
# ============================================================

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_connection():
    conn = get_db()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                subject TEXT,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                icon TEXT,
                link TEXT,
                order_num INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                image_url TEXT,
                category TEXT,
                link TEXT,
                order_num INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                bio TEXT,
                image_url TEXT,
                linkedin_url TEXT,
                order_num INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS testimonials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                quote TEXT NOT NULL,
                rating INTEGER DEFAULT 5,
                image_url TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                value TEXT NOT NULL,
                suffix TEXT DEFAULT '',
                icon TEXT,
                order_num INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute('SELECT COUNT(*) FROM services')
        if cursor.fetchone()[0] == 0:
            insert_default_data(conn)

def insert_default_data(conn):
    cursor = conn.cursor()
    
    services = [
        ('Investment Strategy', 'Customized investment strategies tailored to your financial goals and risk tolerance.', 'chart-line', '/services#strategy', 1),
        ('Portfolio Management', 'Professional management of your investment portfolio to maximize returns.', 'briefcase', '/services#portfolio', 2),
        ('Risk Assessment', 'Comprehensive risk analysis and mitigation strategies.', 'shield-alt', '/services#risk', 3),
        ('Market Research', 'In-depth market research and analysis for informed decisions.', 'search', '/services#research', 4),
        ('Retirement Planning', 'Secure your future with comprehensive retirement planning.', 'umbrella', '/services#retirement', 5),
        ('Wealth Advisory', 'Expert wealth management and advisory services.', 'hand-holding-usd', '/services#wealth', 6),
    ]
    cursor.executemany('INSERT INTO services (title, description, icon, link, order_num) VALUES (?, ?, ?, ?, ?)', services)
    
    portfolio = [
        ('Tech Growth Fund', 'High-growth technology sector investments', 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800', 'tech', '#', 1),
        ('Real Estate Ventures', 'Commercial and residential real estate investments', 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800', 'real-estate', '#', 2),
        ('Green Energy Projects', 'Sustainable and renewable energy investments', 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800', 'energy', '#', 3),
    ]
    cursor.executemany('INSERT INTO portfolio (title, description, image_url, category, link, order_num) VALUES (?, ?, ?, ?, ?, ?)', portfolio)
    
    stats = [
        ('Years Experience', '15', '+', 'calendar', 1),
        ('Happy Clients', '500', '+', 'smile', 2),
        ('Total Investments', '2.5B', '+', 'chart-line', 3),
        ('Team Members', '50', '+', 'users', 4),
    ]
    cursor.executemany('INSERT INTO stats (label, value, suffix, icon, order_num) VALUES (?, ?, ?, ?, ?)', stats)

# ============================================================
# ADMIN ROUTES
# ============================================================

@app.route('/admin')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM contacts WHERE status = "new"')
        new_contacts = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM contacts')
        total_contacts = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM subscribers')
        total_subscribers = cursor.fetchone()[0]
        cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC LIMIT 5')
        recent_contacts = [dict(row) for row in cursor.fetchall()]
        cursor.execute('SELECT COUNT(*) FROM portfolio WHERE is_active = 1')
        active_portfolio = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM services WHERE is_active = 1')
        active_services = cursor.fetchone()[0]
    return render_template('admin/dashboard.html',
                         new_contacts=new_contacts,
                         total_contacts=total_contacts,
                         total_subscribers=total_subscribers,
                         recent_contacts=recent_contacts,
                         active_portfolio=active_portfolio,
                         active_services=active_services)

@app.route('/admin/contacts')
def admin_contacts():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
        contacts = [dict(row) for row in cursor.fetchall()]
    return render_template('admin/contacts.html', contacts=contacts)

@app.route('/admin/contacts/<int:contact_id>/status', methods=['POST'])
def update_contact_status(contact_id):
    data = request.get_json()
    with get_db_connection() as conn:
        conn.execute('UPDATE contacts SET status = ? WHERE id = ?', (data.get('status', 'new'), contact_id))
    return jsonify({'success': True})

@app.route('/admin/services', methods=['GET', 'POST'])
def admin_services():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                cursor.execute('INSERT INTO services (title, description, icon, link, order_num) VALUES (?, ?, ?, ?, ?)',
                             (request.form.get('title'), request.form.get('description'),
                              request.form.get('icon'), request.form.get('link'), request.form.get('order_num', 0)))
            elif action == 'delete':
                cursor.execute('DELETE FROM services WHERE id = ?', (request.form.get('id'),))
            elif action == 'toggle':
                cursor.execute('UPDATE services SET is_active = NOT is_active WHERE id = ?', (request.form.get('id'),))
        cursor.execute('SELECT * FROM services ORDER BY order_num')
        services = [dict(row) for row in cursor.fetchall()]
    return render_template('admin/services.html', services=services)

@app.route('/admin/portfolio', methods=['GET', 'POST'])
def admin_portfolio():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                cursor.execute('INSERT INTO portfolio (title, description, image_url, category, link, order_num) VALUES (?, ?, ?, ?, ?, ?)',
                             (request.form.get('title'), request.form.get('description'),
                              request.form.get('image_url'), request.form.get('category'),
                              request.form.get('link'), request.form.get('order_num', 0)))
            elif action == 'delete':
                cursor.execute('DELETE FROM portfolio WHERE id = ?', (request.form.get('id'),))
        cursor.execute('SELECT * FROM portfolio ORDER BY order_num')
        portfolio = [dict(row) for row in cursor.fetchall()]
    return render_template('admin/portfolio.html', portfolio=portfolio)

@app.route('/admin/subscribers')
def admin_subscribers():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subscribers ORDER BY created_at DESC')
        subscribers = [dict(row) for row in cursor.fetchall()]
    return render_template('admin/subscribers.html', subscribers=subscribers)

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error='Page not found', code=404), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error='Server error', code=500), 500

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    init_db()
    print("\n" + "="*60)
    print("  LIGHTLINE INVESTMENT GROUP - Multi-Site System")
    print("="*60)
    print("  Main Site:           http://127.0.0.1:5000")
    print("  Engineering:         http://127.0.0.1:5000/engineering")
    print("  Logistics:           http://127.0.0.1:5000/logistics")
    print("  Capital:             http://127.0.0.1:5000/capital")
    print("  Research:            http://127.0.0.1:5000/research")
    print("  CFE Training:        http://127.0.0.1:5000/cfe")
    print("  Admin Panel:         http://127.0.0.1:5000/admin")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
