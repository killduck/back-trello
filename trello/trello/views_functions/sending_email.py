from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings

def sending_email(subject_email, text_email, address_mail):
    subject = subject_email
    text_content = text_email
    html_content = render_to_string('mail_template.html', {'data': text_content})
    settings.EMAIL_BACKEND = settings.METHOD['smtp']
    connection = get_connection()
    connection.open()
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[address_mail],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    connection.close()