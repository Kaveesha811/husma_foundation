def send_email(email, message):
    print(f"Email to {email}: {message}")
    # For real email, uncomment and configure:
    # import smtplib
    # from email.mime.text import MIMEText
    # smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # smtp.starttls()
    # smtp.login('your_email@gmail.com', 'your_app_password')
    # msg = MIMEText(message)
    # msg['Subject'] = 'Donation Confirmation'
    # msg['From'] = 'your_email@gmail.com'
    # msg['To'] = email
    # smtp.sendmail('your_email@gmail.com', email, msg.as_string())
    # smtp.quit()
    # Note: Use Gmail app password; enable less secure apps if needed.