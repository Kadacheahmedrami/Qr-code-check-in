import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

base_folder = "users"

def send_email(sender_email, sender_password, recipient_email, subject, body, qr_code_file):
    try:
   
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

   
        msg.attach(MIMEText(body, 'html'))

    
        mime_type, encoding = mimetypes.guess_type(qr_code_file)
        if mime_type is None:
            mime_type = 'application/octet-stream'

    
        with open(qr_code_file, 'rb') as file:
            img = MIMEImage(file.read(), _subtype=mime_type.split('/')[1])  
            img.add_header('Content-ID', '<qr_code_image>')  
            msg.attach(img)

    
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
             
                with open(user_info_file, 'r') as file:
                    user_info = {}
                    for line in file:
                        if "Gmail:" in line:
                            user_info['Gmail'] = line.split(":")[1].strip()
                        if "Full Name:" in line:
                            user_info['Full Name'] = line.split(":")[1].strip()
                
              
                qr_code_file = os.path.join(user_folder_path, "qr_code.png")
              
                subject = "Welcome to Our Platform - Your QR Code"
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
            padding: 0;
            
            margin: 0;
            
        }}
        .container {{
               border: 10px solid #5966F3;
            border-radius: 15px;
            max-width: 600px;
            margin: 0 auto;
        }}
         .double{{
                   font-family: 'Brush Script MT', cursive;
            font-size: 52px;
            font-weight: bold;
       
            color: white;
            background-color: #5966F3;
            

            padding: 20px;
         
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
    
        }}

        .middle-section {{
           
            background-size: cover;
            background-position: center;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .middle-section h1 {{
            color: #4CAF50;
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .middle-section p {{
            font-size: 16px;
            margin-bottom: 20px;
        }}
        .footer {{
        
            background-color: #5966F3;
            color: #fff;
            text-align: center;
            padding: 20px;
            font-size: 14px;
           
        }}
        .footer a {{
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
        .row{{
            font-size: 30px;
            font-weight: 900;
        }}
        .im {{
            width: 50px;
        }}
        .im1 {{
            width: 65px;
        }}
        .im2 {{
            width: 50px;
            margin-left: auto;
        }}
        .im3 {{
            width: 120px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Top Section -->
       <div class="double">
                <p> SIRIUS 101 <br> is here !! </p>
          
        </div>
        <!-- Middle Section -->
        <div class="middle-section">
            <h1>Welcome to the Sirius 101 Workshop!</h1>
            <p>Dear <strong>{user_info['Full Name']}</strong>,</p>
            <p>Congratulations! You have been accepted to the *Sirius 101 Workshop*. We are thrilled to have you join us for this exciting learning experience!</p>
            <p>Below is your unique QR code. Please present it upon arrival to check in:</p>
            <img src="cid:qr_code_image" alt="Your QR Code">
            <p>We can't wait to see you there!</p>
         
         
        </div>

        <!-- Footer Section -->
        <div class="footer">
         
            <div class="row">
                <p><em>Date:</em> 22/23 november<br>
                    <em>Time:</em> 9 AM<br>
                    <em>Location:</em> uknown</p>
            </div>
        </div>
    </div>
</body>
</html>


                """
                
              
                send_email(sender_email, sender_password, user_info['Gmail'], subject, body, qr_code_file)

# there is an option you should activate before u start sending gmails
# 
# check this link : https://www.youtube.com/watch?v=g_j6ILT-X0k 

sender_email = ""  # place the sirius gmail in here
sender_password = ""  # sirius password in here
send_emails_from_users_folder(sender_email, sender_password)
