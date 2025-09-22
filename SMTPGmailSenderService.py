import smtplib
from email.message import EmailMessage

class SMTPGmailSenderService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.username ="brandonvilla694@gmail.com"
        self.password = "bzjq yzbd laly dnov"

    def send(self, to_address, subject, body):
        msg = EmailMessage()
        msg["From"] = self.username
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.username, self.password)
            server.send_message(msg)

    