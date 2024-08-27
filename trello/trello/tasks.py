from .celery import app
#import requests
#import json
#import time
from datetime import datetime
from .models import Card, CardUser, User
from .serializers import CardSerializer, UserSerializer
from .views_functions.sending_email import sending_email

@app.task #регистриуем таску
def repeat_order_make():
    count = 0
    date_now = datetime.now().strftime("%Y-%m-%dT%H:%M:00")
    # print(len(CardSerializer(Card.objects.all(), many=True).data))
    for card in CardSerializer(Card.objects.all(), many=True).data:
        # print(f'233__ {card['date_end'] == date_now}')
        if card['date_end'] == date_now:
            card_users = CardUser.objects.values('user').filter(card_id=card['id'])
            card_users_data = UserSerializer(User.objects.filter(id__in=card_users), many=True).data
            for user in card_users_data:
                subject_email = f'Срок карточки \"{card["name"]}\" истёк.'
                text_email = (f'{user["first_name"]} {user["last_name"]}, '
                              f'у карточки \"{card['name']}\", в которой Вы являетесь участником или '
                              f'подписаны, вышел срок.')
                address_mail = user['email']
                sending_email(subject_email, text_email, address_mail)
                print(f'add_card_due_date test__37\n')

            count += 1

    return f'найдено {count} совпадения/-й + {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
