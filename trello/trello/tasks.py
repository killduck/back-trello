from .celery import app
#import requests
#import json
#import time
from datetime import datetime, timedelta
from .models import Card, CardUser, User
from .serializers import CardSerializer, UserSerializer
from .views_functions.sending_email import sending_email

@app.task # регистрируем таску
def checking_expired_cards():
    count = 0
    datetime_now = datetime.now().strftime("%Y-%m-%dT%H:%M:00")
    datetime_3_hours_before = (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:00")
    print('15', datetime_3_hours_before)
    cards_with_end_date = CardSerializer(Card.objects.filter(date_end__isnull=False), many=True).data
    for card in cards_with_end_date:
        if datetime_3_hours_before < card['date_end'] <= datetime_now:
            card_users = CardUser.objects.values('user').filter(card_id=card['id'])
            card_users_data = UserSerializer(User.objects.filter(id__in=card_users), many=True).data
            for user in card_users_data:
                subject_email = f'Срок карточки \"{card["name"]}\" истёк.'
                text_email = (f'{user["first_name"]} {user["last_name"]}, '
                              f'у карточки \"{card['name']}\", в которой Вы являетесь участником или '
                              f'подписаны, вышел срок.')
                address_mail = user['email']
                sending_email(subject_email, text_email, address_mail)
            count += 1
    return f'найдено {count} совпадения/-й + {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
