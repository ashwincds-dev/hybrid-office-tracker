# Quick Start Guide - 5 Minutes Setup! ⚡

Get the Hybrid Office Tracker running in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
cd /Users/av001/Documents/brm/hybrid-office-webapp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Run the App (30 seconds)

```bash
python app.py
```

You should see:

```
============================================================
🚀 Hybrid Office Tracker - Web Application
============================================================
📍 Running on: http://localhost:5000
👤 Default admin: admin@company.com / admin123
============================================================
```

## Step 3: Open Browser (30 seconds)

Go to: **http://localhost:5000**

## Step 4: Login (1 minute)

Use the default credentials:
- **Email**: admin@company.com
- **Password**: admin123

## Step 5: Set Your Location (1 minute)

1. Click **"Set Location for Tomorrow"**
2. Select your office (e.g., HSR Office)
3. Done! ✅

## Step 6: Invite Your Team (1 minute)

Share the URL with your team:
- They can register at: http://localhost:5000/register
- Everyone sets their location daily
- View team summary on dashboard

---

## What Now?

### For Team Members
- **Every Evening**: Set tomorrow's location
- **Every Morning**: Check who's where today
- **Coordinate**: Plan meetings, carpools, lunches!

### For Admins
- Go to **Admin Panel** to manage users
- View statistics and monitor engagement
- Customize offices in `config.yaml`

---

## Need Production Deployment?

### Quick Docker Deployment

```bash
# Build and run
docker build -t office-tracker .
docker run -d -p 5000:5000 --name office-tracker office-tracker

# Done! Access at http://your-server-ip:5000
```

### Or Docker Compose

```bash
docker-compose up -d
```

---

## Customization

### Change Office Locations

Edit `config.yaml`:

```yaml
offices:
  - name: "Your Office Name"
    emoji: "🏢"
    color: "#4CAF50"
```

### Change Reminder Time

Edit `config.yaml`:

```yaml
schedule:
  evening_reminder: "18:00"  # Change to 6 PM
```

---

## Troubleshooting

**Can't access http://localhost:5000?**
- Check if another app is using port 5000
- Try: `lsof -i :5000`
- Run on different port: `python app.py` (edit app.py)

**Dependencies error?**
- Make sure Python 3.8+ is installed
- Run: `python3 --version`

**Database error?**
- Delete `data/` folder and restart
- It will recreate automatically

---

## What's Next?

- Read **README.md** for full documentation
- See **DEPLOYMENT_GUIDE.md** for production setup
- Customize **config.yaml** for your needs

---

**That's it! You're all set! 🎉**

Need help? Check the README or open an issue.

