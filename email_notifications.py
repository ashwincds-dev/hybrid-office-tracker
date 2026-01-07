"""
Email notifications module for sending reminders
Optional feature - can be enabled in config.yaml
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


class EmailNotifier:
    def __init__(self):
        self.enabled = config.get('email', {}).get('enabled', False)
        if self.enabled:
            self.smtp_host = config['email']['smtp_host']
            self.smtp_port = config['email']['smtp_port']
            self.from_email = config['email']['from_email']
            self.from_name = config['email'].get('from_name', 'Office Tracker')
            self.password = os.environ.get('EMAIL_PASSWORD', '')
    
    def send_evening_reminder(self, user_email, user_name):
        """Send evening reminder to user to set their location"""
        if not self.enabled:
            print(f"📧 [DEMO] Would send reminder to {user_name} ({user_email})")
            return True
        
        subject = "🏢 Set Your Office Location for Tomorrow"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">🏢 Office Tracker</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f9f9f9;">
                <h2>Hi {user_name}! 👋</h2>
                
                <p style="font-size: 16px; line-height: 1.6;">
                    It's time to set your office location for tomorrow!
                </p>
                
                <p style="font-size: 16px; line-height: 1.6;">
                    Please take a moment to let your team know where you'll be working.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/dashboard" 
                       style="background-color: #667eea; color: white; padding: 15px 30px; 
                              text-decoration: none; border-radius: 25px; font-weight: bold;
                              display: inline-block;">
                        Set My Location
                    </a>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 30px;">
                    This helps your teammates coordinate and plan their day!
                </p>
            </div>
            
            <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
                <p>Hybrid Office Tracker • Automated Reminder</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_body)
    
    def send_morning_summary(self, admin_email, summary_data):
        """Send morning summary to admin/team leads"""
        if not self.enabled:
            print(f"📧 [DEMO] Would send morning summary to {admin_email}")
            return True
        
        subject = "📊 Today's Office Locations Summary"
        
        # Build summary HTML
        locations_html = ""
        for location in summary_data:
            locations_html += f"""
            <div style="margin-bottom: 20px; padding: 15px; background-color: white; 
                        border-left: 4px solid {location['color']}; border-radius: 5px;">
                <h3 style="margin: 0 0 10px 0;">
                    <span style="font-size: 1.5em;">{location['emoji']}</span>
                    {location['name']}
                </h3>
                <p style="font-size: 18px; font-weight: bold; margin: 0;">
                    {location['count']} people
                </p>
            </div>
            """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">📊 Daily Summary</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f9f9f9;">
                <h2>Today's Office Locations</h2>
                
                {locations_html}
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="http://localhost:5000/dashboard" 
                       style="background-color: #667eea; color: white; padding: 12px 25px; 
                              text-decoration: none; border-radius: 20px;
                              display: inline-block;">
                        View Full Dashboard
                    </a>
                </div>
            </div>
            
            <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
                <p>Hybrid Office Tracker • Daily Summary</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(admin_email, subject, html_body)
    
    def _send_email(self, to_email, subject, html_body):
        """Internal method to send email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False


# Example usage
if __name__ == "__main__":
    notifier = EmailNotifier()
    
    # Test evening reminder
    notifier.send_evening_reminder("user@example.com", "John Doe")
    
    # Test morning summary
    summary_data = [
        {'name': 'HSR Office', 'emoji': '🏢', 'color': '#4CAF50', 'count': 5},
        {'name': 'Work From Home', 'emoji': '🏠', 'color': '#9C27B0', 'count': 3}
    ]
    notifier.send_morning_summary("admin@example.com", summary_data)

