import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(receiver_email, subject, message):
    smtp_server = "smtp.mailersend.net"
    smtp_port = 587
    smtp_username=os.environ["SMTP_USER"]
    smtp_password=os.environ["SMTP_PASS"]
    msg = MIMEMultipart()
    msg["From"] = os.environ["MAIL_FROM"]
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
    finally:
        server.quit()


# send_email("aditya.sen1hl@gmail.com","123","hi")
