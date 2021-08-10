from django.conf import settings
from django.core.mail import EmailMultiAlternatives


import functools
import math
import threading


def get_unix_time(dt):
    timestamp = dt.timestamp()
    unix_time = math.trunc(timestamp)

    return unix_time


def swagger_fake(fake_retval=None):
    """
    A decorator for a view that returns the provided value
    if being run in the context of swagger schema generation;
    (as per https://github.com/axnsan12/drf-yasg/issues/333#issuecomment-474883875)
    this is intended to be applied to "get_queryset" and/or "get_object"
    """
    def _decorator(view_fn):
        @functools.wraps(view_fn)
        def _wrapper(*args, **kwargs):
            if not args:
                # if this decorator is applied to a CBV using "method_decorator",
                # This conversation was marked as resolved by allynt
                # then view_fn will actually be an instance of functools.partial;
                # I have to introspect it to get the view it was called w/
                _self = view_fn.func.__self__
            else:
                # if this decorator is applied directly to a fn,
                # then the 1st argument will be the view it was called w/
                _self = args[0]

            if getattr(_self, "swagger_fake_view", False):
                return fake_retval

            return view_fn(*args, **kwargs)

        return _wrapper

    return _decorator


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
