from cryptography.fernet import Fernet
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import string
import random

from server.secrets import ENCRYPT_SECRET_KEY


def validate_email(email):
  # https://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python
  from django.core.validators import validate_email
  from django.core.exceptions import ValidationError
  try:
    validate_email(email)
    return True
  except ValidationError:
    return False


def encrypt(data):
  f = Fernet(ENCRYPT_SECRET_KEY)
  return f.encrypt(data.encode())


def decrypt(data):
  f = Fernet(ENCRYPT_SECRET_KEY)
  return f.decrypt(data.decode())


def random_token(length):
  letters = string.ascii_lowercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str


def sendemail(subject, template, context, email_to):
  html_message = render_to_string(template, context)
  plain_message = strip_tags(html_message)

  email_from = 'stamatevalentin64@gmail.com'

  send_mail(subject=subject, message=plain_message, from_email=email_from,
            recipient_list=email_to, html_message=html_message, fail_silently=False)
