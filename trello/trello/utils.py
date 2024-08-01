from django.conf import settings

from django.core.mail import send_mail


class PreparingMessage:

    def __init__(self,
                 subject_letter = 'Letter without subject',
                 text_letter = '',
                ):


        self.__subject_letter = subject_letter
        self.__text_letter = text_letter

    @property
    def get_test(self):
        letter = {
            'subject_letter': self.__subject_letter,
            'text_letter': settings.MAIL_MESSAGE['test'],
        }
        return letter

    @property
    def get_empty(self):
        letter = {
            'subject_letter': self.__subject_letter,
            'text_letter': self.__text_letter,
        }
        return letter

    @property
    def get_add_dashboard(self):
        letter = {
            'subject_letter': self.__subject_letter,
            'text_letter': settings.MAIL_MESSAGE['add_dashboard'] + self.__text_letter,
        }
        return letter

    @property
    def get_deadline(self):
        letter = {
            'subject_letter': self.__subject_letter,
            'text_letter': settings.MAIL_MESSAGE['deadline'] + self.__text_letter,
        }
        return letter




class SendMessage:

    def __init__(self,
                 letter,
                 method,
                 fail_silently,
                 sender_email,
                ):

        self.__letter = letter
        self.__method = method
        self.__fail_silently = fail_silently
        self.__sender_email = sender_email

    @property
    def get_send_email(self):

        settings.EMAIL_BACKEND = settings.METHOD[self.__method] if self.__method != None else settings.METHOD['console']

        send_mail (
            self.__letter['subject_letter'],
            self.__letter['text_letter'],
            self.__sender_email if self.__sender_email != None else settings.EMAIL_HOST_USER,
            self.__letter['addres_mail'],
            self.__fail_silently
        )


class HashMessage:

    def __init__(self, message):
        self.__message = message

    @property
    def get_hash_message(self):
        pass
