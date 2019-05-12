from django.http import UnreadablePostError

# https://docs.djangoproject.com/zh-hans/2.0/topics/logging/#id5
def skip_unreadable_post(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        if isinstance(exc_value, UnreadablePostError):
            return False
    return True

