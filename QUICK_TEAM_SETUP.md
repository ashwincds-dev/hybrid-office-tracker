# 🚀 Quick Team Setup - 5 Minutes!

## Your Application is Running! Here's How to Share It:

---

## 🎯 Your Network URL

**Share this with your team:**

```
http://192.168.0.109:5000
```

---

## ⚡ Quick Setup (If Teammates Can't Access)

Your Mac firewall is **enabled**, which might block teammates. Here's how to fix:

### Option A: Allow Python Through Firewall (Recommended)

Run these commands in your terminal:

```bash
# Find Python path
which python3

# Add Python to firewall exceptions
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add $(which python3)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp $(which python3)

# Verify
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getappblocked $(which python3)
```

It will ask for your password - this is normal!

### Option B: Temporarily Disable Firewall

1. Open **System Settings** (or System Preferences)
2. Go to **Network** → **Firewall**
3. Click the lock and enter password
4. **Turn off** Firewall
5. Turn back on after testing

---

## 🧪 Test if It's Working

### From Your Machine:

```bash
curl http://192.168.0.109:5000/health
```

You should see:
```json
{
    "status": "healthy",
    "database": "connected"
}
```

### From Teammate's Computer:

Ask them to:
1. Open browser
2. Go to: **http://192.168.0.109:5000**
3. Should see the Office Tracker landing page

Or test with curl:
```bash
curl http://192.168.0.109:5000
```

---

## 📋 Team Onboarding Steps

### Step 1: Share the URL
Send this message to your team:

```
Hi Team! 👋

I've set up our Hybrid Office Tracker!

🌐 Access it here: http://192.168.0.109:5000

📝 To get started:
1. Click "Register"
2. Enter your name and email
3. Create a password
4. Set your location for tomorrow!

Every evening, just login and set where you'll be tomorrow.
Every morning, check the dashboard to see where everyone is! 🏢

Questions? Let me know!
```

### Step 2: Help Them Register

Each teammate should:
1. Open http://192.168.0.109:5000
2. Click **"Register"**
3. Fill in:
   - Name: Their full name
   - Email: Their work email
   - Password: At least 6 characters
4. Click **"Register"**
5. Login with their credentials

### Step 3: First Location Set

After login, they'll see:
1. **Dashboard**
2. Button: "Set Location for Tomorrow"
3. Choose: HSR Office / MDP Office / Intuit Office / WFH / Day Off
4. Done! ✅

---

## 🎯 Daily Workflow

### Evening (Before 7 PM):
Everyone logs in and sets tomorrow's location (takes 10 seconds)

### Morning:
Check the dashboard to see who's where today!

---

## ⚠️ Important Notes

### Your Machine Must Stay On
- ✅ Keep your Mac awake
- ✅ Don't close the laptop lid (or disable sleep)
- ✅ Keep connected to WiFi

### Everyone Must Be on Same WiFi
- ✅ Same office network
- ✅ Or connected to company VPN
- ❌ Won't work from home (unless VPN)

### IP Might Change
If you reconnect to WiFi, your IP might change. Check it with:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

If it changes, update your team with the new URL.

---

## 🔥 Prevent Mac from Sleeping

So your teammates can always access:

### Option 1: System Settings
1. **System Settings** → **Battery**
2. **Turn off** "Put hard disks to sleep"
3. Set "Display off when inactive" to Never (while plugged in)

### Option 2: Terminal Command
```bash
# Prevent sleep while command runs
caffeinate -d -i -m -s
```

Or while app runs:
```bash
caffeinate -i python app.py
```

---

## 🚀 Alternative: Remote Team Access

If teammates are working from home or different locations:

### Quick Option: Use ngrok (5 minutes)

```bash
# Install ngrok
brew install ngrok

# Sign up at https://ngrok.com and get auth token
ngrok config add-authtoken YOUR_TOKEN

# Create tunnel
ngrok http 5000

# Share the https URL shown (e.g., https://abc123.ngrok-free.app)
```

### Permanent Option: Cloud Server

Deploy to DigitalOcean, Heroku, or AWS for permanent internet access.
See `TEAM_DEPLOYMENT_GUIDE.md` for full instructions.

---

## 🆘 Troubleshooting

### Problem: "Connection refused"

**Solution 1:** Check if app is running
```bash
ps aux | grep "python app.py"
```

**Solution 2:** Restart the app
```bash
cd /Users/av001/Documents/brm/hybrid-office-webapp
source venv/bin/activate
python app.py
```

**Solution 3:** Check firewall (see above)

### Problem: "Can't reach this page"

**Solution 1:** Verify everyone is on same WiFi
```bash
# Your IP: 192.168.0.109
# Teammate should have IP like 192.168.0.x
```

**Solution 2:** Check your IP didn't change
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Problem: Page loads slowly

**Solution:** Too many users for development server. 

Either:
- Use Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- Or deploy to cloud server

---

## 📊 Check Current Status

### Is App Running?
```bash
ps aux | grep "python app.py"
```

### How Many Users?
```bash
cd /Users/av001/Documents/brm/hybrid-office-webapp
sqlite3 data/office_tracker.db "SELECT COUNT(*) FROM users;"
```

### Who's Registered?
```bash
sqlite3 data/office_tracker.db "SELECT name, email FROM users;"
```

### Today's Responses?
```bash
sqlite3 data/office_tracker.db "SELECT COUNT(*) FROM responses WHERE date = date('now');"
```

---

## 📱 Share This Quick Guide

Send your team this simple message:

```
🏢 Office Tracker Setup

1. Open: http://192.168.0.109:5000
2. Register with your name & email
3. Set your location for tomorrow
4. Done! 

Every evening: Login and set tomorrow's location
Every morning: Check where everyone is

Questions? Just ask!
```

---

## ✅ Summary

**Your setup:**
- ✅ App running on: http://192.168.0.109:5000
- ⚠️ Firewall enabled (allow Python if teammates can't access)
- 👥 Ready for team to register and use!

**Next steps:**
1. Allow Python through firewall (see above)
2. Share URL with team: http://192.168.0.109:5000
3. Help first few teammates register
4. Start coordinating! 🎉

---

**Need more help?** Check `TEAM_DEPLOYMENT_GUIDE.md` for cloud deployment and other options!

