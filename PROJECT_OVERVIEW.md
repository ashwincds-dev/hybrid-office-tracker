# Hybrid Office Tracker - Web Application
## Complete Project Overview & Guide

This document contains everything you need to understand, deploy, and use the Hybrid Office Tracker web application.

---

## 📋 Table of Contents

1. [What Is This?](#what-is-this)
2. [Why Web Application?](#why-web-application)
3. [Project Structure](#project-structure)
4. [Quick Start (5 Minutes)](#quick-start)
5. [Features Overview](#features-overview)
6. [Technology Stack](#technology-stack)
7. [Configuration](#configuration)
8. [Deployment Options](#deployment-options)
9. [User Guide](#user-guide)
10. [Admin Guide](#admin-guide)
11. [API Documentation](#api-documentation)
12. [Troubleshooting](#troubleshooting)

---

## What Is This?

The Hybrid Office Tracker is a web-based solution for coordinating office locations in a hybrid work environment. It helps teams know who's working from which office each day.

### The Problem It Solves

In hybrid work:
- ❓ You don't know who's in the office today
- ❓ Hard to plan in-person meetings
- ❓ Carpooling coordination is difficult
- ❓ Can't easily find teammates for lunch

### The Solution

- ✅ Everyone sets their location daily
- ✅ Dashboard shows who's where
- ✅ Calendar tracks history
- ✅ Automated reminders
- ✅ Beautiful, mobile-friendly interface

---

## Why Web Application?

### Advantages Over Other Solutions

**vs. Slack Bot:**
- ✅ Universal access (no Slack required)
- ✅ Works for external users (contractors, partners)
- ✅ Fully customizable UI
- ✅ No platform dependency
- ✅ Lower setup complexity

**vs. Spreadsheets:**
- ✅ No manual updates
- ✅ Automated reminders
- ✅ Better UI/UX
- ✅ Historical tracking
- ✅ User authentication

**vs. Commercial Solutions:**
- ✅ Self-hosted (data control)
- ✅ Free and open source
- ✅ Customizable
- ✅ No recurring fees

---

## Project Structure

```
hybrid-office-webapp/
│
├── 📄 Core Application Files
│   ├── app.py                      # Main Flask application (500+ lines)
│   ├── email_notifications.py     # Email reminder system
│   ├── requirements.txt            # Python dependencies
│   └── config.yaml                 # Configuration file
│
├── 🎨 Templates (HTML Pages)
│   ├── base.html                   # Base layout with Bootstrap 5
│   ├── index.html                  # Landing page
│   ├── login.html                  # Login page
│   ├── register.html               # User registration
│   ├── dashboard.html              # Main dashboard
│   ├── calendar.html               # Personal calendar view
│   ├── summary.html                # Daily team summary
│   └── admin.html                  # Admin panel
│
├── 📚 Documentation
│   ├── README.md                   # Main documentation
│   ├── QUICKSTART.md              # 5-minute setup guide
│   ├── DEPLOYMENT_GUIDE.md        # Production deployment
│   ├── COMPARISON.md              # vs Slack Bot comparison
│   └── PROJECT_OVERVIEW.md        # This file
│
├── 🐳 Deployment Files
│   ├── Dockerfile                  # Docker container
│   ├── docker-compose.yml         # Docker Compose config
│   └── .gitignore                 # Git ignore rules
│
└── 📁 Runtime (Generated)
    └── data/
        └── office_tracker.db       # SQLite database
```

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 5 minutes of your time

### Installation Steps

```bash
# 1. Navigate to the project directory
cd /Users/av001/Documents/brm/hybrid-office-webapp

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py
```

### Access the Application

1. Open your browser
2. Go to: **http://localhost:5000**
3. Login with default admin credentials:
   - **Email:** admin@company.com
   - **Password:** admin123

### First Steps

1. **Change Admin Password** (recommended)
2. **Invite Team Members** - Share registration link
3. **Customize Offices** - Edit `config.yaml`
4. **Set Your Location** - Click "Set Location for Tomorrow"

---

## Features Overview

### 🔐 Authentication System

- **User Registration** - Email-based signup
- **Secure Login** - Password hashing with Werkzeug
- **Session Management** - Flask sessions with secure cookies
- **Admin Panel** - User management interface

### 📅 Daily Planning

- **Set Tomorrow's Location** - Evening check-in
- **View Today's Status** - See your current location
- **Change Location** - Update anytime before morning
- **Location History** - Track past selections

### 👥 Team Visibility

- **Dashboard Summary** - See where everyone is today
- **Detailed Lists** - Team members grouped by location
- **No Response Tracking** - See who hasn't checked in
- **Real-time Updates** - Instant visibility

### 📊 Calendar & History

- **Personal Calendar** - View your location history
- **Date-based Summary** - See any past or future date
- **Statistics** - Track patterns and trends
- **Export Options** - (Coming soon)

### 👨‍💼 Admin Features

- **User Management** - Activate/deactivate users
- **Statistics Dashboard** - Response rates, active users
- **Office Configuration** - Manage locations
- **Bulk Operations** - (Coming soon)

### 🔔 Notifications

- **Evening Reminders** - Scheduled at 7 PM (configurable)
- **Email Integration** - Optional SMTP setup
- **In-app Notifications** - Flash messages
- **Customizable Messages** - Edit in config.yaml

---

## Technology Stack

### Backend

- **Framework:** Flask 3.0 (Python)
- **Database:** SQLite (upgradeable to PostgreSQL)
- **Scheduler:** APScheduler
- **Security:** Werkzeug Security
- **Configuration:** PyYAML

### Frontend

- **UI Framework:** Bootstrap 5.3
- **Icons:** Bootstrap Icons
- **JavaScript:** Vanilla JS (no framework)
- **Styling:** Custom CSS + Bootstrap

### Deployment

- **Container:** Docker
- **Orchestration:** Docker Compose
- **Web Server:** Gunicorn (production)
- **Reverse Proxy:** Nginx (recommended)

---

## Configuration

### config.yaml Structure

```yaml
schedule:
  evening_reminder: "19:00"      # When to send reminders
  timezone: "Asia/Kolkata"       # Your timezone
  skip_weekends: true            # Skip Sat/Sun

app:
  name: "Hybrid Office Tracker"
  company: "Your Company Name"

offices:
  - name: "HSR Office"
    emoji: "🏢"
    color: "#4CAF50"
  - name: "MDP Office"
    emoji: "🏛️"
    color: "#2196F3"
  - name: "Intuit Office"
    emoji: "🏭"
    color: "#FF9800"
  - name: "Work From Home"
    emoji: "🏠"
    color: "#9C27B0"
  - name: "Day Off"
    emoji: "🌴"
    color: "#F44336"

email:
  enabled: false                 # Enable email notifications
  smtp_host: "smtp.gmail.com"
  smtp_port: 587
  from_email: "noreply@company.com"
```

### Environment Variables

Create a `.env` file (optional):

```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
EMAIL_PASSWORD=your-email-password
```

### Customization Examples

**Change office locations:**
```yaml
offices:
  - name: "Bangalore Office"
    emoji: "🏢"
    color: "#4CAF50"
  - name: "Mumbai Office"
    emoji: "🌆"
    color: "#2196F3"
```

**Change reminder time:**
```yaml
schedule:
  evening_reminder: "18:30"  # 6:30 PM instead of 7 PM
```

**Change timezone:**
```yaml
schedule:
  timezone: "America/New_York"  # US Eastern Time
```

---

## Deployment Options

### Option 1: Local Development

```bash
python app.py
```

Access at: http://localhost:5000

### Option 2: Docker

```bash
# Build and run
docker build -t office-tracker .
docker run -d -p 5000:5000 --name office-tracker office-tracker

# Or use Docker Compose
docker-compose up -d
```

### Option 3: Production Server (Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 4: Cloud Platforms

**AWS EC2:**
- Launch Ubuntu instance
- Install Python + dependencies
- Run with systemd service
- Use Nginx as reverse proxy

**Heroku:**
```bash
heroku create your-office-tracker
git push heroku main
```

**DigitalOcean:**
- Use App Platform
- Connect GitHub repo
- Auto-deploy

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

---

## User Guide

### For Team Members

#### Daily Workflow

**Evening (Before 7 PM):**
1. Log in to the dashboard
2. Click "Set Location for Tomorrow"
3. Select your office location
4. Done! ✅

**Morning:**
1. Check dashboard to see where everyone is
2. Coordinate with teammates at same location
3. Plan meetings, carpools, or lunch

#### Using the Dashboard

The dashboard shows:
- **Today's Location** - Where you are now
- **Tomorrow's Location** - What you've set (or prompt to set)
- **Team Summary** - Statistics by location
- **Detailed List** - Everyone grouped by office

#### Viewing Your History

1. Click "Calendar" in navigation
2. See your location history
3. Track patterns over time

### For New Users

#### Registration

1. Go to: http://your-server:5000/register
2. Enter your name and email
3. Create a password (min 6 characters)
4. Click "Register"
5. Login with your credentials

#### First-Time Setup

1. Login with your credentials
2. Set tomorrow's location immediately
3. Explore the dashboard
4. Check the calendar view
5. Bookmark the site!

---

## Admin Guide

### Accessing Admin Panel

1. Login with admin account
2. Click "Admin" in navigation
3. View statistics and user list

### Managing Users

**Activate/Deactivate User:**
- Click "Deactivate" to disable a user (they can't login)
- Click "Activate" to re-enable them
- Inactive users don't appear in summaries

**Creating First Admin:**
Default admin is created automatically:
- Email: admin@company.com
- Password: admin123

**⚠️ Change this immediately after first login!**

### Monitoring

**Statistics:**
- Active Users count
- Responses Today count
- Response rate trends

**Logs:**
```bash
# View application logs
tail -f logs/app.log

# Or with Docker
docker logs -f office-tracker
```

### Database Management

**Backup:**
```bash
cp data/office_tracker.db backups/office_tracker_$(date +%Y%m%d).db
```

**Reset:**
```bash
rm data/office_tracker.db
python app.py  # Will recreate with fresh data
```

**Query:**
```bash
sqlite3 data/office_tracker.db
sqlite> SELECT * FROM users;
sqlite> SELECT * FROM responses WHERE date = '2026-01-07';
```

---

## API Documentation

### Authentication Required

All API endpoints require authentication (login session).

### Endpoints

#### GET /api/locations
Get all active office locations.

**Response:**
```json
[
  {
    "id": 1,
    "name": "HSR Office",
    "emoji": "🏢",
    "color": "#4CAF50",
    "is_active": 1
  },
  ...
]
```

#### GET /api/summary/{date}
Get summary for a specific date.

**Example:** `/api/summary/2026-01-07`

**Response:**
```json
[
  {
    "name": "HSR Office",
    "emoji": "🏢",
    "color": "#4CAF50",
    "count": 5,
    "users": "Alice, Bob, Charlie, David, Emma"
  },
  ...
]
```

#### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-07T10:30:00+05:30"
}
```

---

## Troubleshooting

### Common Issues

#### Can't Login

**Problem:** Invalid email or password error

**Solutions:**
- Check email spelling
- Verify password is correct
- Try resetting via admin panel
- Check if account is active

#### App Won't Start

**Problem:** Error when running `python app.py`

**Solutions:**
```bash
# Check Python version
python --version  # Need 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check port availability
lsof -i :5000

# Try different port (edit app.py)
```

#### Database Errors

**Problem:** "database is locked" or similar

**Solutions:**
```bash
# Close all connections
# Stop the app
# Delete database and restart
rm data/office_tracker.db
python app.py
```

#### Can't Access from Other Devices

**Problem:** Works on localhost but not from phone/other PC

**Solutions:**
```bash
# Make sure app runs on 0.0.0.0
# Check firewall settings
# Use your local IP: http://192.168.1.xxx:5000
```

#### Email Notifications Not Working

**Problem:** Reminders not being sent

**Solutions:**
1. Check `config.yaml` - `email.enabled: true`
2. Set `EMAIL_PASSWORD` environment variable
3. Check SMTP settings
4. Test email manually with `email_notifications.py`

### Getting Help

1. Check the logs: `tail -f logs/app.log`
2. Review `DEPLOYMENT_GUIDE.md`
3. Check GitHub issues (if applicable)
4. Contact system administrator

---

## File Contents Reference

### Key Application Files

#### app.py (Main Application)

Contains:
- Flask app initialization
- Database schema and functions
- All route handlers (@app.route)
- Authentication decorators
- Scheduler for evening reminders
- API endpoints

Key functions:
- `init_db()` - Initialize database
- `seed_initial_data()` - Create default data
- `login_required` - Auth decorator
- `send_evening_reminders()` - Scheduler job
- Various route handlers for pages

#### email_notifications.py (Optional)

Contains:
- `EmailNotifier` class
- `send_evening_reminder()` method
- `send_morning_summary()` method
- Email templates with HTML
- SMTP configuration

#### config.yaml (Configuration)

Sections:
- `schedule` - Reminder times and timezone
- `app` - Application metadata
- `offices` - Office location definitions
- `email` - SMTP settings (optional)

### Template Files

All templates extend `base.html` which provides:
- Bootstrap 5 styling
- Navigation bar
- Flash message handling
- Responsive layout
- Custom CSS

Individual templates:
- `index.html` - Marketing/landing page
- `login.html` - Login form
- `register.html` - Registration form
- `dashboard.html` - Main user interface
- `calendar.html` - History view
- `summary.html` - Date-specific summary
- `admin.html` - Admin control panel

---

## Database Schema

### Tables

#### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### locations
```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    emoji TEXT NOT NULL,
    color TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1
);
```

#### responses
```sql
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    date DATE NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
    UNIQUE(user_id, date)
);
```

#### notifications
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## Security Considerations

### Built-in Security

✅ **Password Hashing** - Werkzeug's secure hashing
✅ **Session Management** - Flask sessions
✅ **SQL Injection Protection** - Parameterized queries
✅ **XSS Protection** - Template escaping
✅ **CSRF Protection** - (Add Flask-WTF for forms)

### Production Recommendations

1. **Change Secret Key**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Use HTTPS**
```bash
# Get free SSL certificate
sudo certbot --nginx -d office.yourcompany.com
```

3. **Set Strong Password Policy**
```python
# In registration, enforce:
- Minimum 8 characters
- Require uppercase, lowercase, number
- Check against common passwords
```

4. **Regular Backups**
```bash
# Daily backup cron job
0 2 * * * /opt/office-tracker/backup.sh
```

5. **Update Dependencies**
```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

---

## Roadmap & Future Features

### Planned Features

- [ ] Email notifications fully integrated
- [ ] SMS reminders (Twilio)
- [ ] Push notifications (PWA)
- [ ] Mobile apps (React Native)
- [ ] Calendar integrations (Google, Outlook)
- [ ] Slack/Teams webhooks
- [ ] Analytics dashboard
- [ ] Export to CSV/PDF
- [ ] Bulk import users
- [ ] Multi-company support
- [ ] Advanced reporting
- [ ] API rate limiting
- [ ] OAuth2 support
- [ ] SSO integration

### Contributing

Want to add features? The codebase is well-structured:

1. **Backend** - Add routes in `app.py`
2. **Frontend** - Add templates in `templates/`
3. **Database** - Modify schema in `init_db()`
4. **Config** - Add settings to `config.yaml`

---

## Support & Resources

### Documentation Files

- `README.md` - Main documentation
- `QUICKSTART.md` - Fast setup guide
- `DEPLOYMENT_GUIDE.md` - Production deployment
- `COMPARISON.md` - vs Slack Bot
- `PROJECT_OVERVIEW.md` - This comprehensive guide

### External Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Bootstrap 5: https://getbootstrap.com/
- SQLite: https://www.sqlite.org/
- Docker: https://docs.docker.com/

---

## Summary

**What You Have:**
A complete, production-ready web application for hybrid office coordination with:

- ✅ Beautiful, responsive UI
- ✅ User authentication
- ✅ Admin panel
- ✅ Calendar tracking
- ✅ Scheduled reminders
- ✅ Docker deployment
- ✅ Complete documentation

**How to Get Started:**
```bash
cd /Users/av001/Documents/brm/hybrid-office-webapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

**Default Login:**
- Email: admin@company.com
- Password: admin123

---

**Built with ❤️ for hybrid teams everywhere! 🏢**

*Last Updated: January 7, 2026*

