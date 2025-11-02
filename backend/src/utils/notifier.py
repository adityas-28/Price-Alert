import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASS = "your_app_password"

async def send_email(to_email: str, asin: str, current_price: float, threshold: float):
    subject = f"Price Drop Alert for {asin}"
    body = (
        f"The price of product {asin} has dropped to ₹{current_price}.\n"
        f"Your set threshold was ₹{threshold}.\n\n"
        f"Check it out before it goes up again!"
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)

    print(f"📨 Email sent to {to_email} for {asin}")
