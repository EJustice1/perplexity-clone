import smtplib
from email.message import EmailMessage
from typing import Optional

class EmailSender:
    """Minimal SMTP sender for Stage 5 fixed content emails."""

    def __init__(self, host: str, port: int, username: Optional[str], password: Optional[str], use_tls: bool = True) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._use_tls = use_tls

    def send_plaintext(self, to_email: str, subject: str, body: str, from_email: str) -> None:
        message = EmailMessage()
        message["To"] = to_email
        message["From"] = from_email
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self._host, self._port) as smtp:
            if self._use_tls:
                smtp.starttls()
            if self._username and self._password:
                smtp.login(self._username, self._password)
            smtp.send_message(message)
