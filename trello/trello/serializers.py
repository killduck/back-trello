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

    cards = CardSerializer(many=True, required=False)

    class Meta:
        model = Column

        fields = (
            "id",
            "name",
            "order",
            "cards",
        )

    # перопределяем метод для записи
    def create(self, validated_data):

        if 'cards' not in self.initial_data:
            # Cоздаём запись если колонка создается без карточек
            column = Column.objects.create(**validated_data)
            return column

        # Уберем список карточек из словаря validated_data и сохраним его cards_data
        cards_data = validated_data.pop('cards')

        # Создадим новую колонку пока без карточек
        column = Column.objects.create(**validated_data)

        # Получаем каждую карточку из списка и создаем новую запись
        for card in cards_data:
            Card.objects.create(column=column, **card)

        return column  # бинго


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person

        fields = (
            "id",
            "first_name",
            "last_name",
            "nick_name",
        )
