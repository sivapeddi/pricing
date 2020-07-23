from requests import Response, post
import os
from typing import List


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:

    FROM_TITLE = 'Pricing service'
    FROM_EMAIL = 'do-not-reply@sandbox6270e3c796c24d63bb246a8da15feafc.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:

        MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
        MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)
        print(email)

        if MAILGUN_API_KEY is None:
            raise MailgunException('Failed to load mailgun api key')
        if MAILGUN_DOMAIN is None:
            raise MailgunException('Failed to load mailgun domain')
        response = post(
            f"{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html}
        )
        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error occurred while sending e-mail.')
        return response