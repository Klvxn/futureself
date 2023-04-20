from datetime import datetime
from gettext import ngettext

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail
from django.conf import settings

from .models import Letter


logger = get_task_logger(__name__)


@shared_task(name='send-futureself-emails')
def send_futureself_emails():
    logger.info('Checking for emails to be delivered today')
    logger.info('Please wait...')
    count = 0
    today = datetime.today().date()
    to_be_delivered = []
    for letter in Letter.objects.all():
        if letter.delivery_date == today and letter.delivered is False:
            count += 1
            to_be_delivered.append(letter)
    if count:
        info = ngettext(
            f'Found {count} email to be delivered',
            f'Found {count} emails to be delivered',
            count
        )
        logger.info(info)
        logger.info('Delivering emails...')
        for letter in to_be_delivered:
            status = send_mail(
                letter.title,
                letter.content,
                settings.DEFAULT_FROM_EMAIL,
                [letter.email_address],
            )
            if status == 1:
                letter.delivered = True
                letter.save()
        info = ngettext(
            f'{count} email delivered successfully',
            f'{count} emails delivered successfully',
            count
        )
        logger.info(info)
    else:
        logger.info('No email to be delivered today.')
