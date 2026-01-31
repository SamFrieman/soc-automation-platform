#!/usr/bin/env python3
"""
Playbook: Send Email Notification
"""

import sys
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_email_notification(alert_data):
    """Send email notification about alert"""
    try:
        EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
        EMAIL_USER = os.getenv('EMAIL_HOST_USER', '')
        EMAIL_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
        ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        
        if not EMAIL_USER or not EMAIL_PASSWORD:
            return False, "Email credentials not configured"
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[{alert_data['severity']}] SOC Alert: {alert_data['title']}"
        msg['From'] = EMAIL_USER
        msg['To'] = ADMIN_EMAIL
        
        # Email body
        html = f"""
        <html>
        <body>
            <h2>Security Alert Detected</h2>
            <p><strong>Alert ID:</strong> {alert_data['alert_id']}</p>
            <p><strong>Severity:</strong> <span style="color: red;">{alert_data['severity']}</span></p>
            <p><strong>Title:</strong> {alert_data['title']}</p>
            <p><strong>Description:</strong> {alert_data['description']}</p>
            <p><strong>Source IP:</strong> {alert_data.get('source_ip', 'N/A')}</p>
            <p><strong>Detected At:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <p>Please investigate this alert in the SOC Platform.</p>
        </body>
        </html>
        """
        
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Send email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True, f"Email sent to {ADMIN_EMAIL}"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"


def main(alert_data):
    """Main execution function"""
    success, message = send_email_notification(alert_data)
    
    return {
        'status': 'SUCCESS' if success else 'FAILED',
        'actions_taken': [{
            'action': 'send_email',
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }],
        'output': message
    }


if __name__ == '__main__':
    alert_data = json.loads(sys.stdin.read())
    result = main(alert_data)
    print(json.dumps(result))