from rest_framework import serializers

from .models import Card, Column, Dashboard, Role, DashboardUserRole


class DashboardUserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DashboardUserRole

        fields = (
            "dashboard",
            "user",
            "role",
        )


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card

        fields = (
            "id",
            "name",
            # "author",
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
            'dashboard',
            "cards",
        )


class DashboardSerializer(serializers.ModelSerializer):

    column = ColumnSerializer(many=True, required=False)
    dashboard_user_role = DashboardUserRoleSerializer(many=True, required=False)

    class Meta:
        model = Dashboard

        fields = (
            'id',
            'name',
            'img',
            'dashboard_user_role',
            'column',
        )


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role

        fields = (
            "id",
            "name",
            "description",
        )


# Пробный вариант сериализатора - пока нигде не применяем
class TestColumnSerializer(serializers.ModelSerializer):

    cards = CardSerializer(many=True, required=False)

    class Meta:
        model = Column

        fields = (
            "id",
            "name",
            "order",
            'dashboard',
            "cards",
        )

    # переопределяем метод для записи
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

        return column
