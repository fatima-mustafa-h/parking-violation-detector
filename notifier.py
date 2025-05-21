import smtplib
from email.message import EmailMessage

def send_email_alert(zone_id, timestamp):
    msg = EmailMessage()
    msg.set_content(f'Violation detected in Zone {zone_id} at {timestamp}')
    msg['Subject'] = f'Parking Violation Alert: Zone {zone_id}'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)
