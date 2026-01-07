# Deployment Guide - Hybrid Office Tracker

Complete guide for deploying the Hybrid Office Tracker web application in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Security Best Practices](#security-best-practices)

---

## Local Development

### Setup

```bash
# Navigate to project directory
cd /Users/av001/Documents/brm/hybrid-office-webapp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

Access at: http://localhost:5000

**Default Admin Credentials:**
- Email: admin@company.com
- Password: admin123

---

## Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With logging
gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile access.log \
  --error-logfile error.log \
  app:app
```

### Systemd Service (Linux)

Create `/etc/systemd/system/office-tracker.service`:

```ini
[Unit]
Description=Hybrid Office Tracker
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/office-tracker
Environment="PATH=/opt/office-tracker/venv/bin"
Environment="SECRET_KEY=your-secret-key-here"
ExecStart=/opt/office-tracker/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
sudo systemctl enable office-tracker
sudo systemctl start office-tracker
sudo systemctl status office-tracker
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/office-tracker`:

```nginx
server {
    listen 80;
    server_name office.yourcompany.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Optional: Static files
    location /static {
        alias /opt/office-tracker/static;
        expires 30d;
    }
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/office-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d office.yourcompany.com
```

---

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./config.yaml:/app/config.yaml:ro
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Build and Run

```bash
# Build image
docker build -t office-tracker .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config.yaml:/app/config.yaml:ro \
  -e SECRET_KEY="your-secret-key" \
  --name office-tracker \
  office-tracker

# Or with Docker Compose
docker-compose up -d

# View logs
docker logs -f office-tracker

# Stop
docker stop office-tracker
```

---

## Cloud Deployment

### AWS EC2

**1. Launch EC2 Instance**
- Ubuntu 22.04 LTS
- t2.micro (free tier)
- Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)

**2. Connect and Setup**

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone/upload your application
sudo mkdir /opt/office-tracker
sudo chown ubuntu:ubuntu /opt/office-tracker
cd /opt/office-tracker

# Upload files (from local machine)
scp -i your-key.pem -r ./* ubuntu@your-ec2-ip:/opt/office-tracker/
```

**3. Setup Application**

```bash
cd /opt/office-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn

# Generate secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**4. Configure Systemd** (see above)

**5. Configure Nginx** (see above)

**6. Get SSL Certificate** (see above)

### Google Cloud Platform

**1. Create VM Instance**
```bash
gcloud compute instances create office-tracker \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server,https-server
```

**2. SSH and Setup**
```bash
gcloud compute ssh office-tracker --zone=us-central1-a
# Follow same steps as AWS EC2
```

### Heroku

**1. Create Heroku App**
```bash
heroku create your-office-tracker

# Add buildpack
heroku buildpacks:set heroku/python
```

**2. Create Procfile**
```
web: gunicorn app:app
```

**3. Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-office-tracker
git push heroku main
```

**4. Set Environment Variables**
```bash
heroku config:set SECRET_KEY="your-secret-key"
```

### DigitalOcean App Platform

**1. Connect GitHub Repo**
- Go to DigitalOcean App Platform
- Connect your repository

**2. Configure App**
```yaml
name: office-tracker
services:
- name: web
  github:
    repo: your-username/office-tracker
    branch: main
  run_command: gunicorn -w 4 -b 0.0.0.0:8080 app:app
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SECRET_KEY
    value: your-secret-key
    type: SECRET
```

---

## Security Best Practices

### 1. Change Default Credentials

```python
# After first login, go to Admin Panel
# Create new admin user
# Delete or disable default admin@company.com
```

### 2. Generate Strong Secret Key

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Update in environment or systemd service:
```bash
export SECRET_KEY="your-generated-key"
```

### 3. Database Backups

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /opt/office-tracker/data/office_tracker.db \
   /opt/backups/office_tracker_$DATE.db

# Keep only last 30 days
find /opt/backups -name "office_tracker_*.db" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /opt/office-tracker/backup.sh
```

### 4. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 5. HTTPS Only

In Nginx config:
```nginx
server {
    listen 80;
    server_name office.yourcompany.com;
    return 301 https://$server_name$request_uri;
}
```

### 6. Rate Limiting

In Nginx:
```nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

location /login {
    limit_req zone=login burst=5;
    # ... rest of config
}
```

### 7. Regular Updates

```bash
# Update dependencies monthly
source venv/bin/activate
pip list --outdated
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart office-tracker
```

### 8. Monitoring

```bash
# Check logs
sudo journalctl -u office-tracker -f

# Check resource usage
htop

# Check disk space
df -h
```

### 9. Environment Variables

Never commit sensitive data! Use:
- `.env` file (git ignored)
- Environment variables
- Secrets manager (AWS Secrets Manager, etc.)

### 10. Database Encryption

For sensitive deployments, consider:
- Encrypting SQLite database
- Using PostgreSQL with encryption
- Storing database on encrypted volume

---

## Performance Optimization

### 1. Database Indexing

Already included in schema, but verify:
```sql
CREATE INDEX IF NOT EXISTS idx_responses_date ON responses(date);
CREATE INDEX IF NOT EXISTS idx_responses_user_date ON responses(user_id, date);
```

### 2. Caching

Add Redis for session caching (optional):
```python
from flask_session import Session
app.config['SESSION_TYPE'] = 'redis'
```

### 3. Static File Serving

Use Nginx for static files:
```nginx
location /static {
    alias /opt/office-tracker/static;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 4. Database Connection Pooling

For high traffic, use connection pooling:
```python
from flask_sqlalchemy import SQLAlchemy
# Configure connection pool
```

---

## Monitoring & Logging

### Application Logs

```bash
# View systemd logs
sudo journalctl -u office-tracker -f

# View Gunicorn logs
tail -f /opt/office-tracker/access.log
tail -f /opt/office-tracker/error.log
```

### Nginx Logs

```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Check Endpoint

Add to `app.py`:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200
```

### Monitoring Tools

- **Uptime**: UptimeRobot, Pingdom
- **Application**: New Relic, DataDog
- **Logs**: Papertrail, Loggly
- **Errors**: Sentry

---

## Troubleshooting

### App Won't Start

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check port availability
sudo lsof -i :5000

# Check permissions
ls -la /opt/office-tracker/data
```

### Database Errors

```bash
# Reset database
rm data/office_tracker.db
python3 app.py  # Will recreate
```

### Permission Errors

```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/office-tracker

# Fix permissions
chmod 755 /opt/office-tracker
chmod 644 /opt/office-tracker/data/office_tracker.db
```

### Nginx Not Working

```bash
# Test config
sudo nginx -t

# Check service
sudo systemctl status nginx

# View errors
sudo tail -f /var/log/nginx/error.log
```

---

## Maintenance

### Weekly Tasks
- Check logs for errors
- Verify backups
- Monitor disk space

### Monthly Tasks
- Update dependencies
- Review user accounts
- Check security updates

### Quarterly Tasks
- Review configuration
- Performance audit
- Security audit

---

For additional help, see README.md or contact your system administrator.

