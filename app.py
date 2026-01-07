#!/usr/bin/env python3
"""
Hybrid Office Tracker - Web Application
Flask backend for office location coordination
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta, date
import sqlite3
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import yaml

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Database path
DATABASE = 'data/office_tracker.db'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Scheduler
scheduler = BackgroundScheduler()
timezone = pytz.timezone(config['schedule']['timezone'])


# Database helper functions
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Office locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            emoji TEXT NOT NULL,
            color TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Responses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            location_id INTEGER NOT NULL,
            date DATE NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (location_id) REFERENCES locations(id),
            UNIQUE(user_id, date)
        )
    ''')
    
    # Notifications log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT NOT NULL,
            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_responses_date ON responses(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_responses_user_date ON responses(user_id, date)')
    
    conn.commit()
    conn.close()


def cleanup_duplicate_locations():
    """Remove duplicate locations, keep only the first occurrence"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Get all location names with their first ID
        cursor.execute('''
            SELECT name, MIN(id) as keep_id
            FROM locations
            GROUP BY name
            HAVING COUNT(*) > 1
        ''')
        duplicates = cursor.fetchall()
        
        for dup in duplicates:
            # Delete all duplicates except the first one
            cursor.execute('''
                DELETE FROM locations 
                WHERE name = ? AND id != ?
            ''', (dup['name'], dup['keep_id']))
            print(f"✅ Cleaned up duplicates for: {dup['name']}")
        
        conn.commit()
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
    finally:
        conn.close()


def seed_initial_data():
    """Seed initial office locations and admin user"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Insert default locations (OR IGNORE if already exist)
    locations = [
        ('HSR Office', '🏢', '#4CAF50'),
        ('MDP Office', '🏛️', '#2196F3'),
        ('Intuit Office', '🏭', '#FF9800'),
        ('Work From Home', '🏠', '#9C27B0'),
        ('Day Off', '🌴', '#F44336')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO locations (name, emoji, color) VALUES (?, ?, ?)',
        locations
    )
    
    # Check if admin user exists (by email)
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE email = ?', ('admin@company.com',))
    if cursor.fetchone()['count'] == 0:
        # Create default admin user
        admin_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (email, name, password_hash, is_admin)
            VALUES (?, ?, ?, ?)
        ''', ('admin@company.com', 'Admin User', admin_password, True))
    
    conn.commit()
    conn.close()


# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not user['is_admin']:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# Routes
@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND is_active = 1', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['is_admin'] = user['is_admin']
            
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate inputs
        if not current_password or not new_password or not confirm_password:
            flash('All fields are required', 'error')
            return render_template('change_password.html')
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('change_password.html')
        
        # Check minimum length
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('change_password.html')
        
        # Verify current password
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], current_password):
            conn.close()
            flash('Current password is incorrect', 'error')
            return render_template('change_password.html')
        
        # Update password
        new_password_hash = generate_password_hash(new_password)
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', 
                      (new_password_hash, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('change_password.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Email already registered', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (email, name, password_hash)
            VALUES (?, ?, ?)
        ''', (email, name, password_hash))
        
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get today's date
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Get user's response for today
    cursor.execute('''
        SELECT l.name, l.emoji, l.color
        FROM responses r
        JOIN locations l ON r.location_id = l.id
        WHERE r.user_id = ? AND r.date = ?
    ''', (session['user_id'], today))
    today_location = cursor.fetchone()
    
    # Get user's response for tomorrow
    cursor.execute('''
        SELECT l.id, l.name, l.emoji, l.color
        FROM responses r
        JOIN locations l ON r.location_id = l.id
        WHERE r.user_id = ? AND r.date = ?
    ''', (session['user_id'], tomorrow))
    tomorrow_location = cursor.fetchone()
    
    # Get all active locations
    cursor.execute('SELECT * FROM locations WHERE is_active = 1')
    locations = cursor.fetchall()
    
    # Get today's summary
    cursor.execute('''
        SELECT l.name, l.emoji, l.color, COUNT(*) as count
        FROM responses r
        JOIN locations l ON r.location_id = l.id
        WHERE r.date = ?
        GROUP BY l.id
        ORDER BY count DESC
    ''', (today,))
    today_summary = cursor.fetchall()
    
    # Get team members at each location today
    cursor.execute('''
        SELECT u.name as user_name, l.name as location_name, l.emoji, l.color
        FROM responses r
        JOIN users u ON r.user_id = u.id
        JOIN locations l ON r.location_id = l.id
        WHERE r.date = ? AND u.is_active = 1
        ORDER BY l.name, u.name
    ''', (today,))
    team_locations = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html',
                         today=today,
                         tomorrow=tomorrow,
                         today_location=today_location,
                         tomorrow_location=tomorrow_location,
                         locations=locations,
                         today_summary=today_summary,
                         team_locations=team_locations)


@app.route('/set-location', methods=['POST'])
@login_required
def set_location():
    """Set user's office location for a date"""
    location_id = request.form.get('location_id', type=int)
    target_date = request.form.get('date')
    
    if not location_id or not target_date:
        return jsonify({'success': False, 'message': 'Missing parameters'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Insert or update response
    cursor.execute('''
        INSERT INTO responses (user_id, location_id, date)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, date)
        DO UPDATE SET location_id = ?, timestamp = CURRENT_TIMESTAMP
    ''', (session['user_id'], location_id, target_date, location_id))
    
    conn.commit()
    conn.close()
    
    flash('Location updated successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/summary/<date_str>')
@login_required
def summary(date_str):
    """View summary for a specific date"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format', 'error')
        return redirect(url_for('dashboard'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get summary
    cursor.execute('''
        SELECT l.name, l.emoji, l.color, COUNT(*) as count
        FROM responses r
        JOIN locations l ON r.location_id = l.id
        WHERE r.date = ?
        GROUP BY l.id
        ORDER BY count DESC
    ''', (target_date,))
    summary_data = cursor.fetchall()
    
    # Get detailed list
    cursor.execute('''
        SELECT u.name as user_name, l.name as location_name, l.emoji, l.color
        FROM responses r
        JOIN users u ON r.user_id = u.id
        JOIN locations l ON r.location_id = l.id
        WHERE r.date = ? AND u.is_active = 1
        ORDER BY l.name, u.name
    ''', (target_date,))
    detailed_list = cursor.fetchall()
    
    # Get users who haven't responded
    cursor.execute('''
        SELECT u.name
        FROM users u
        WHERE u.is_active = 1
        AND u.id NOT IN (
            SELECT user_id FROM responses WHERE date = ?
        )
        ORDER BY u.name
    ''', (target_date,))
    no_response = cursor.fetchall()
    
    conn.close()
    
    return render_template('summary.html',
                         date=target_date,
                         summary=summary_data,
                         detailed_list=detailed_list,
                         no_response=no_response)


@app.route('/calendar')
@login_required
def calendar():
    """Calendar view of user's responses"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user's responses for the last 30 days and next 30 days
    start_date = date.today() - timedelta(days=30)
    end_date = date.today() + timedelta(days=30)
    
    cursor.execute('''
        SELECT r.date, l.name, l.emoji, l.color
        FROM responses r
        JOIN locations l ON r.location_id = l.id
        WHERE r.user_id = ? AND r.date BETWEEN ? AND ?
        ORDER BY r.date
    ''', (session['user_id'], start_date, end_date))
    
    user_responses = cursor.fetchall()
    conn.close()
    
    return render_template('calendar.html',
                         responses=user_responses,
                         start_date=start_date,
                         end_date=end_date)


@app.route('/admin')
@admin_required
def admin_panel():
    """Admin panel"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute('''
        SELECT id, email, name, is_admin, is_active, created_at
        FROM users
        ORDER BY name
    ''')
    users = cursor.fetchall()
    
    # Get all locations
    cursor.execute('SELECT * FROM locations ORDER BY name')
    locations = cursor.fetchall()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as total FROM users WHERE is_active = 1')
    stats = {'active_users': cursor.fetchone()['total']}
    
    cursor.execute('SELECT COUNT(*) as total FROM responses WHERE date = ?', (date.today(),))
    stats['responses_today'] = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('admin.html', users=users, locations=locations, stats=stats)


@app.route('/admin/users/toggle/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user(user_id):
    """Toggle user active status"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET is_active = NOT is_active WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    flash('User status updated', 'success')
    return redirect(url_for('admin_panel'))


# API endpoints
@app.route('/api/locations')
@login_required
def api_locations():
    """Get all active locations"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM locations WHERE is_active = 1')
    locations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(locations)


@app.route('/api/summary/<date_str>')
@login_required
def api_summary(date_str):
    """Get summary for a specific date"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT l.name, l.emoji, l.color, COUNT(*) as count,
               GROUP_CONCAT(u.name, ', ') as users
        FROM responses r
        JOIN users u ON r.user_id = u.id
        JOIN locations l ON r.location_id = l.id
        WHERE r.date = ? AND u.is_active = 1
        GROUP BY l.id
    ''', (date_str,))
    
    summary = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(summary)


@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    try:
        # Check database connectivity
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now(timezone).isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now(timezone).isoformat()
        }), 500


# Scheduled tasks
def send_evening_reminders():
    """Send evening reminders (placeholder for email integration)"""
    if not should_run_today():
        return
    
    conn = get_db()
    cursor = conn.cursor()
    
    tomorrow = date.today() + timedelta(days=1)
    
    # Get users who haven't set location for tomorrow
    cursor.execute('''
        SELECT u.id, u.email, u.name
        FROM users u
        WHERE u.is_active = 1
        AND u.id NOT IN (
            SELECT user_id FROM responses WHERE date = ?
        )
    ''', (tomorrow,))
    
    users_to_remind = cursor.fetchall()
    
    for user in users_to_remind:
        # Log reminder (in production, send actual email)
        cursor.execute('''
            INSERT INTO notifications (user_id, type)
            VALUES (?, 'evening_reminder')
        ''', (user['id'],))
        print(f"📧 Would send reminder to {user['name']} ({user['email']})")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Evening reminders processed: {len(users_to_remind)} users")


def should_run_today():
    """Check if should run today (skip weekends if configured)"""
    if config['schedule'].get('skip_weekends', True):
        today = datetime.now(timezone).weekday()
        return today < 5  # Monday=0, Friday=4
    return True


def setup_scheduler():
    """Setup scheduled jobs"""
    evening_time = config['schedule']['evening_reminder'].split(':')
    
    scheduler.add_job(
        send_evening_reminders,
        trigger=CronTrigger(
            hour=int(evening_time[0]),
            minute=int(evening_time[1]),
            timezone=timezone
        ),
        id='evening_reminders',
        replace_existing=True
    )
    
    print(f"✅ Scheduled evening reminders at {config['schedule']['evening_reminder']} {timezone}")


# Initialize database and scheduler (for production/gunicorn)
try:
    init_db()
    cleanup_duplicate_locations()  # Clean up any duplicates
    seed_initial_data()
    setup_scheduler()
    scheduler.start()
    print("✅ App initialized (database + scheduler)")
except Exception as e:
    print(f"⚠️  Initialization warning: {e}")


if __name__ == '__main__':
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Initialize database
    init_db()
    seed_initial_data()
    
    # Setup scheduler
    setup_scheduler()
    scheduler.start()
    
    print("\n" + "="*60)
    print("🚀 Hybrid Office Tracker - Web Application")
    print("="*60)
    print(f"📍 Running on: http://localhost:5000")
    print(f"👤 Default admin: admin@company.com / admin123")
    print("="*60 + "\n")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

