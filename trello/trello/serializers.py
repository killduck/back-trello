from rest_framework import serializers

from .models import Card, Column, Dashboard, Role, DashboardUserRole, User


class UserSerializer(serializers.ModelSerializer):

    first_letter = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "first_letter",
        )

    def get_first_letter(self, obj):
        return obj.username[:1].upper()


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role

        fields = (
            "id",
            "name",
            "description",
        )


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card

        fields = (
            "id",
            "name",
            "order",
            "column",
            "date_start",
            "date_end",
            "label",
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


class DashboardUserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False)

    class Meta:
        model = DashboardUserRole

        fields = (
            "dashboard",
            "user",
            "role",
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
            'column',
            'dashboard_user_role',
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
