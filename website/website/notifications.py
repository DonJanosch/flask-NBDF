from datetime import datetime, timedelta
from dateutil.parser import parse
from flask_login import current_user
from flask_mail import Mail, Message

from website import email_scheduler, app

def resolve_datetime(datetime_str:str):
    return parse(datetime_str)

def schedule_new_email(topic:str, message:str, notification_time:datetime):
    if current_user.is_authenticated:
        recipient = current_user.email
        email_scheduler.add_job(send_email(recipient, topic, message), 'date', run_date=notification_time, args=[datetime.now()])

def send_email(recipient, topic, message):
    msg = Message(
    topic,
    sender=app.config['MAIL_USERNAME'],
    recipients=[recipient]
    )
    msg.body = message
    mail.send(msg)
