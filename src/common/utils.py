from django.conf import settings
from django.core.mail import EmailMultiAlternatives


import functools
import math
import threading


def get_unix_time(dt):
    timestamp = dt.timestamp()
    unix_time = math.trunc(timestamp)

    return unix_time


class EmailThread(threading.Thread):
    def __init__(self, subject, body, recipient_list, html=None, from_email=None, fail_silently=False):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.html = html
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.body, self.from_email, self.recipient_list)

        if self.html:
            msg.attach_alternative(self.html, 'text/html')

        msg.send(self.fail_silently)
