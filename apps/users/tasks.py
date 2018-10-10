import logging

from PIL import Image
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from multilibrary.celery import app


@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your Multilibrary account',
            'Hey, looks like you wanna start to use Multilibrary! So hurry up: follow the link to verify your account: '
            'http://localhost:8000%s' % reverse('verify_post', kwargs={'uuid': str(user.verification_uuid)}),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)


@app.task
def save_thumbnail(user_pk, thumb_abs_path, user_avatar_path):
    try:
        width = 200
        thumbnail = Image.open(user_avatar_path)
        resize_percent = (width / float(thumbnail.size[0]))
        height = int((float(thumbnail.size[1])*float(resize_percent)))
        thumbnail = thumbnail.resize((width, height), Image.ANTIALIAS)
        thumbnail.save(thumb_abs_path)
    except Exception as error:
        logging.error("User_pk=%s. Error: %s" % (user_pk, type(error)))
