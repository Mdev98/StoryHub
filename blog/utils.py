import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]


def send_email(destination: str, subject: str, html: str):
    params = {
        "from": "noreply@samad-invest.com",
        "to": [destination],
        "subject": subject,
        "html": html
    }
    email = resend.Emails.send(params)

