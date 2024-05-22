from rest_framework import serializers

from .models import Card, Column, Person


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card

        fields = (
            "id",
            "name",
            "author",
            "order",
            "column",
        )

class ColumnSerializer(serializers.ModelSerializer):

    cards = CardSerializer(many=True)

    class Meta:
        model = Column

        fields = (
            "id",
            "name",
            "order",
            "cards",
        )

    def create(self, validated_data):  # перопределяем метод для записи
        # Уберем список карточек из словаря validated_data и сохраним его
        cards = validated_data.pop('cards')

        # Создадим новую колонку пока без достижений, тк данных нам достаточно
        column = Column.objects.create(**validated_data)
        # print('validated_data=>',validated_data, 'cards=>', cards)

        # Получаем каждую карточку из списка
        # for card in cards:
        #     print('Карточка=>', card)
            # Создадим новую запись или получим существующий экземпляр из БД
            # current_card, status = Card.objects.get_or_create(**card)

            # Card.objects.create(card=current_card, cat=cat)

        return column


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person

        fields = (
            "id",
            "first_name",
            "last_name",
            "nick_name",
        )
