from flask_mail import Message
from flask import render_template
from app import app, mail
from threading import Thread


def send_async_email(app, msg):
    # This function runs in a separate thread and sends the email asynchronously
    with app.app_context():
        mail.send(msg)

# Send emails asynchronously
def send_email(subject, sender, recipients, text_body, html_body):
    # This function is used to send an email
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    # This function sends a password reset email to the user
    token = user.get_reset_password_token()
    send_email('[Insert+] Reset Your Password',
               sender=app.config['MAIL_DEFAULT_SENDER'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
