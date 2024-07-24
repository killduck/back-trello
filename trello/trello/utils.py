from django.conf import settings

# from django.core.mail import send_mail


class Letter:

    def __init__(self,
                 subject_letter,
                 text_letter,
                 addres_mail,
                 method='console',
                 sender_email=settings.EMAIL_HOST_USER,
                 fail_silently=False,
                ):

        self.__subject_letter = subject_letter
        self.__text_letter = text_letter
        self.__addres_mail = addres_mail
        self.__method = settings.METHOD[method]
        self.__sender_email = sender_email
        self.__fail_silently = fail_silently


    def _get_message(self):
        INFO_MESSAGE = (
            f'Отправитель: {self.__sender_email} \n'
            f'Получатель: {self.__addres_mail} \n'
            f'Тема: {self.__subject_letter} \n'
            f'Текст сообщения: {self.__text_letter}'
        )
        return INFO_MESSAGE

    def _get_letter(self):
        letter = {
            'subject_letter': self.__subject_letter,
            'text_letter': self.__text_letter,
            'sender_email': self.__sender_email,
            'addres_mail': [self.__addres_mail],
            'fail_silently': self.__fail_silently,
            'method': self.__method
        }
        return letter



class SendMessage:

    def __init__(self, letter):
        self.__letter = letter

    def _send_email(self):

        # settings.EMAIL_BACKEND = settings.METHOD[self.__letter.method]

        return (
            self.__letter.subject_letter,
            self.__letter.text_letter,
            self.__letter.sender_email,
            [self.__letter.addres_mail],
            self.__letter.fail_silently
        )



test_letter = Letter(
    'Тема письма',
    'Сообщение письма',
    'raa@nmgk.ru',
)

print(test_letter)
