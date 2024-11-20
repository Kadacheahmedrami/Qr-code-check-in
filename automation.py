import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

base_folder = "users"

def send_email(sender_email, sender_password, recipient_email, subject, body, qr_code_file):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add the email body
        msg.attach(MIMEText(body, 'html'))

        # Attach the QR code image
        mime_type, encoding = mimetypes.guess_type(qr_code_file)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        with open(qr_code_file, 'rb') as file:
            img = MIMEImage(file.read(), _subtype=mime_type.split('/')[1])
            img.add_header('Content-ID', '<qr_code_image>')
            msg.attach(img)

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

def send_emails_from_users_folder(sender_email, sender_password):
    for user_folder in os.listdir(base_folder):
        user_folder_path = os.path.join(base_folder, user_folder)
        if os.path.isdir(user_folder_path):
            user_info_file = os.path.join(user_folder_path, "user_info.txt")
            if os.path.exists(user_info_file):
                # Read user information
                with open(user_info_file, 'r') as file:
                    user_info = {}
                    for line in file:
                        if "Gmail:" in line:
                            user_info['Gmail'] = line.split(":")[1].strip()
                        if "Full Name:" in line:
                            user_info['Full Name'] = line.split(":")[1].strip()

                qr_code_file = os.path.join(user_folder_path, "qr_code.png")

                # Email details
                subject = "🎉 Congratulations, You're in Sirius 101! 🚀"
                body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sirius 101 Workshop - Acceptance</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 90%;
            width: 600px;
            margin: 20px auto;
            border: 8px solid #5966F3;
            border-radius: 15px;
            background-color: #fff;
        }}
        .header {{
            background-color: #5966F3;
            color: white;
            text-align: center;
            padding: 30px 20px;
            font-family: 'Brush Script MT', cursive;
            font-size: 48px;
            font-weight: bold;
        }}
        .middle-section {{
            padding: 20px;
            text-align: center;
        }}
        .middle-section h1 {{
            font-size: 24px;
            color: #4CAF50;
            margin-bottom: 10px;
        }}
        .middle-section p {{
            font-size: 16px;
            line-height: 1.5;
        }}
        .middle-section img {{
            max-width: 80%;
            height: auto;
            margin: 20px 0;
         
        }}
        .qr{{
               border: 2px solid #5966F3;
            border-radius: 10px;
        }}
        .footer {{
            background-color: #5966F3;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 14px;
        }}
        .footer a {{
            color: white;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header"> Sirius 101 </div>
        <div class="middle-section">
            <h1>Welcome, {user_info['Full Name']}!</h1>
            <p>We are thrilled to welcome you to <strong>Sirius 101</strong>! 🌟</p>
            <p>You have earned your spot in this exciting journey of innovation and learning! 🎓⚡</p>
            <p>📅 <strong>Event Details:</strong></p>
            <p>🗓️ <strong>Date:</strong> November 22 & 23<br>
               📍 <strong>Location:</strong> ESTIN</p>
            <p>Your unique QR code is below. Please present it upon arrival for check-in:</p>
            <img class="qr" src="cid:qr_code_image" alt="Your QR Code">
            <p>We can’t wait to see you shine! ✨</p>
        </div>
        <div class="footer">
            <p>Stay connected with us for updates:</p>
            <p><a href="https://sirius101.vercel.app">🌐 Website</a> | <a href="https://www.instagram.com/sirius.estin/">📸 Instagram</a></p>
        </div>
    </div>
</body>
</html>
                """

                send_email(sender_email, sender_password, user_info['Gmail'], subject, body, qr_code_file)

# Gmail credentials
sender_email = ""
sender_password = ""

send_emails_from_users_folder(sender_email, sender_password)
