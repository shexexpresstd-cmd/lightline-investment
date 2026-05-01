from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import sqlite3
import os

main_bp = Blueprint('main', __name__,
                    template_folder='../templates/main',
                    url_prefix='')

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lightline_investment.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@main_bp.route('/')
def index():
    conn = get_db()
    services = conn.execute('SELECT * FROM services WHERE is_active=1 ORDER BY order_num').fetchall()
    portfolio = conn.execute('SELECT * FROM portfolio WHERE is_active=1 ORDER BY order_num').fetchall()
    team = conn.execute('SELECT * FROM team WHERE is_active=1 ORDER BY order_num').fetchall()
    testimonials = conn.execute('SELECT * FROM testimonials WHERE is_active=1 ORDER BY created_at DESC').fetchall()
    stats = conn.execute('SELECT * FROM stats WHERE is_active=1 ORDER BY order_num').fetchall()
    conn.close()
    return render_template('main/index.html',
                         services=services, portfolio=portfolio,
                         team=team, testimonials=testimonials, stats=stats)

@main_bp.route('/about')
def about():
    conn = get_db()
    team = conn.execute('SELECT * FROM team WHERE is_active=1 ORDER BY order_num').fetchall()
    stats = conn.execute('SELECT * FROM stats WHERE is_active=1 ORDER BY order_num').fetchall()
    conn.close()
    return render_template('main/about.html', team=team, stats=stats)

@main_bp.route('/services')
def services():
    conn = get_db()
    services = conn.execute('SELECT * FROM services WHERE is_active=1 ORDER BY order_num').fetchall()
    conn.close()
    return render_template('main/services.html', services=services)

@main_bp.route('/portfolio')
def portfolio():
    conn = get_db()
    portfolio = conn.execute('SELECT * FROM portfolio WHERE is_active=1 ORDER BY order_num').fetchall()
    conn.close()
    return render_template('main/portfolio.html', portfolio=portfolio)

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@main_bp.route('/subsidiaries')
def subsidiaries():
    return render_template('main/subsidiaries.html')

@main_bp.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.json
    conn = get_db()
    conn.execute('INSERT INTO contacts (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)',
                 (data['name'], data['email'], data.get('phone', ''), data.get('subject', ''), data['message']))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Thank you! We will get back to you soon.'})

@main_bp.route('/api/subscribe', methods=['POST'])
def api_subscribe():
    data = request.json
    conn = get_db()
    try:
        conn.execute('INSERT INTO subscribers (email) VALUES (?)', (data['email'],))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Successfully subscribed!'})
    except:
        conn.close()
        return jsonify({'success': False, 'message': 'Email already subscribed.'})
