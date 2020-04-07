import os
from typing import List
from requests import post, Response

from models.user.error import MailGunException
from dotenv import load_dotenv

load_dotenv()

class MailGun:
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMIAN', None)

    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = "Do-not-reply@sandboxa4dda5509119442fb2d7de6a77c0f0c2.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        if cls.MAILGUN_API_KEY == None:
            raise MailGunException("Failed to load a API Key")
        if cls.MAILGUN_DOMAIN == None:
            raise MailGunException("Failed to load a mailgun domain name!")
        response = post(f"{cls.MAILGUN_DOMAIN}/messages",
                        auth=("api", cls.MAILGUN_API_KEY),
                        data={
                            "from": f"{cls.FROM_TITLE}<{cls.FROM_EMAIL}>",
                            "to": email,
                            "subject": subject,
                            "text": text,
                            "html": html})
        if response.status_code != 200:
            print(response.json())
            raise MailGunException('An error occurred while sending an e-mail.')
        return response


