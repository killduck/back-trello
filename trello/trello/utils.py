from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class PreparingMessage:

    def __init__(self,
                 template,
                 subject_letter = 'Letter without subject',
                 text_letter = '',
                ):


        self.__subject_letter = subject_letter
        self.__text_letter = text_letter
        self.__template = template

    @property
    def get_message(self):
        letter = {
            'subject_letter': self.__subject_letter,
            'text_letter': settings.MAIL_MESSAGE.get(self.__template, '') + self.__text_letter,
        }
        return letter


class SendMessage:

    def __init__(self,
                 letter,
                 addres_mail,
                 sender_email = settings.EMAIL_HOST_USER,
                 fail_silently = True,
                ):

        self.__letter = letter
        self.__addres_mail = addres_mail
        self.__sender_email = sender_email
        self.__fail_silently = fail_silently


    def __send(self, html_content=''):
        send_mail (
            self.__letter['subject_letter'],
            strip_tags(self.__letter['text_letter']),
            self.__sender_email,
            self.__addres_mail,
            self.__fail_silently,
            html_message=html_content,
        )

    @property
    def get_send_email(self):
        settings.EMAIL_BACKEND = settings.METHOD['smtp']

        html_content = render_to_string('mail_template.html', {'data': self.__letter['text_letter']})

        self.__send(html_content)

    @property
    def get_write_to_file(self):
        settings.EMAIL_BACKEND = settings.METHOD['file']
        self.__send()

    @property
    def get_output_to_console(self):
        settings.EMAIL_BACKEND = settings.METHOD['console']
        self.__send()


class HashMessage:

    def __init__(self, message):
        self.__message = message

    @property
    def get_hash_message(self):
        pass
