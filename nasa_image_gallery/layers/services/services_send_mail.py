from django.core.mail import send_mail
from django.conf import settings

def send(email, username):
    subject = "Verificación de cuenta"
    body = "Hola " + username + ", usted ha creado una cuenta para la galería de la nasa"

    send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)