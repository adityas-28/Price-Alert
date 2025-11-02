import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SENDER_EMAIL, SENDER_PASS
import asyncio

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

async def send_email(to_email: str, asin: str, current_price: float, threshold: float):
    subject = f"Price Drop Alert for {asin}"
    body = (
        f"The price of the product '{asin}' has dropped to ₹{current_price}.\n"
        f"Your set threshold was ₹{threshold}.\n\n"
        f"Check it out before it goes up again!"
    )

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    def _send():  # <-- make this synchronous
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASS)
                server.send_message(msg)
            print(f"Email sent to {to_email} for {asin}")
        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")

    # Run the blocking SMTP part in a separate thread
    await asyncio.to_thread(_send)
