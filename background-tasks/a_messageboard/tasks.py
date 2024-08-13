from django.core.mail import EmailMessage
from celery import shared_task
from django.template.loader import render_to_string
from .models import MessageBoard
from datetime import datetime

@shared_task(name="email_notification")
def send_email_thread(subject, body, emailaddress):
        email = EmailMessage(subject, body, 'kunalarya873@gmail.com', [emailaddress])
        email.send()
        return emailaddress


@shared_task(name="monthly_newsletter")
def send_newsletter(name="monthly_newsletter"):
    subject = "Your Monthly Newsletter"

    subscribers = MessageBoard.objects.get(id=1).subscribers.all()

    for subscriber in subscribers:
        body = render_to_string('a_messageboard/newsletter.html', {'name': subscriber.profile.name})
        email = EmailMessage( subject, body, to=[subscriber.email] )
        email.content_subtype = "html"
        email.send()
    current_month = datetime.now().strftime('%B')
    subscriber_count = subscribers.count()
    return f'{current_month} Newsletter to {subscriber_count} subs'

