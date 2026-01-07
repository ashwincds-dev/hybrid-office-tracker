# Hybrid Office Tracker - Web Application

A modern, self-hosted web application for coordinating office locations in a hybrid work environment. Know where your team members will be working each day!

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🏢 **Multiple Office Locations** - Support for multiple offices (HSR, MDP, Intuit, WFH, Day Off)
- 📅 **Daily Planning** - Set your location for tomorrow, view today's status
- 👥 **Team Visibility** - See where everyone will be working
- 📊 **Calendar View** - Track your location history
- 🔐 **User Authentication** - Secure login/registration system
- 👨‍💼 **Admin Panel** - Manage users and view statistics
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔔 **Evening Reminders** - Scheduled reminders at 7 PM (configurable)
- 🎨 **Modern UI** - Beautiful, intuitive interface with Bootstrap 5

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone or navigate to the directory
cd /Users/av001/Documents/brm/hybrid-office-webapp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Access the Application

1. Open your browser and go to: **http://localhost:5000**
2. Login with the default admin account:
   - **Email**: admin@company.com
   - **Password**: admin123

3. 🎉 Start using the app!

## 📖 User Guide

### For Team Members

1. **Register** - Create an account with your email and name
2. **Set Location** - Every evening, set where you'll be tomorrow
3. **View Team** - See where everyone else will be
4. **Check Calendar** - View your location history

### Daily Workflow

**Evening (Before 7 PM):**
- Login to the dashboard
- Click "Set Location for Tomorrow"
- Select your office location
- Done! ✅

**Morning:**
- Check the dashboard to see where everyone is today
- Coordinate with teammates at the same location

## 🎨 Screenshots

### Dashboard
- View today's location
- Set tomorrow's location
- See team summary

### Calendar View
- Track your location history
- Plan ahead

### Admin Panel
- Manage users
- View statistics
- Monitor office locations

## 🔧 Configuration

Edit `config.yaml` to customize:

```yaml
schedule:
  evening_reminder: "19:00"  # When to send reminders
  timezone: "Asia/Kolkata"   # Your timezone
  skip_weekends: true        # Skip weekends

offices:
  - name: "HSR Office"
    emoji: "🏢"
    color: "#4CAF50"
  # Add more offices...
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Scheduler**: APScheduler
- **Authentication**: Werkzeug Security

## 📂 Project Structure

```
hybrid-office-webapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── config.yaml           # Configuration file
├── data/                 # Database directory
│   └── office_tracker.db
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── calendar.html
│   ├── summary.html
│   └── admin.html
└── docs/                 # Documentation
```

## 🚢 Deployment

### Option 1: Docker (Recommended)

```bash
docker build -t office-tracker .
docker run -d -p 5000:5000 --name office-tracker office-tracker
```

### Option 2: Production Server (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Cloud Deployment

See `DEPLOYMENT_GUIDE.md` for detailed instructions on:
- AWS EC2
- Google Cloud
- Heroku
- DigitalOcean

## 🔐 Security

- Passwords are hashed using Werkzeug's secure password hashing
- Session management with secure cookies
- Change the `SECRET_KEY` in production
- Use HTTPS in production environments
- Regular security updates recommended

## 📧 Email Notifications (Optional)

To enable email reminders, update `config.yaml`:

```yaml
email:
  enabled: true
  smtp_host: "smtp.gmail.com"
  smtp_port: 587
  from_email: "noreply@yourcompany.com"
```

And set the EMAIL_PASSWORD environment variable.

## 🧪 Testing

```bash
# Run in test mode
FLASK_ENV=development python app.py

# Access the app
http://localhost:5000
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 💡 Tips & Best Practices

1. **Set location daily** - Make it a habit to set your location every evening
2. **Check team summary** - Review who's where before planning meetings
3. **Use calendar view** - Track patterns and plan ahead
4. **Admin: Review stats** - Monitor response rates and engagement

## 🆘 Support & Troubleshooting

### Common Issues

**Can't login?**
- Check email and password
- Try resetting (use admin panel)

**App not starting?**
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 5000 is available

**Database errors?**
- Delete `data/office_tracker.db` to reset
- Restart the application

### Getting Help

1. Check `DEPLOYMENT_GUIDE.md`
2. Review logs in console
3. Check GitHub issues
4. Contact your admin

## 🎯 Roadmap

- [ ] Email notifications integration
- [ ] Push notifications (PWA)
- [ ] Mobile app (React Native)
- [ ] Calendar integrations (Google Calendar, Outlook)
- [ ] Slack/Teams integration
- [ ] Analytics dashboard
- [ ] Multi-company support
- [ ] API documentation

## 👏 Acknowledgments

Built with ❤️ for hybrid teams everywhere!

---

**Made with 🏢 by the Hybrid Work Team**

