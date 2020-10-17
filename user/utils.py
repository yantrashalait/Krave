import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .auth_tokens import account_activation_token

User = get_user_model()


def send_user_verification_email(user_id):
    """
    Sends email to the user with content as link to verify the user.
    :param user_id: Integer field
    :return: None
    """
    user = User.objects.get(id=user_id)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Activate Account"
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email
    domain = settings.SITE_URL

    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = account_activation_token.make_token(user)

    html = """
                <html>
                    <head></head>
                    <body>
                        Hi """ + user.username + """,
                        Please click
                        <a href=" """ + domain + """/api/v1/activate/?uidb64=""" + uid + """&token=""" + token + """ "> here </a>
                        to complete your registration
                    </body>
                </html>
            """

    html_part = MIMEText(html, 'html')
    msg.attach(html_part)

    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_HOST_USER, [user.email, ], msg.as_string())
    server.quit()
