from django.core.validators import validate_email
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from tickets.models import Message, Ticket


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщения"""
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Message
        fields = ['created_time', 'user', 'text']


class StuffTicketSerializer(serializers.ModelSerializer):
    """Сериализатор тикета для персонала"""
    user = serializers.CharField(source='user.username', read_only=True)
    messages = MessageSerializer(source='get_tickets_messages', many=True, required=False)

    class Meta:
        model = Ticket
        fields = ['type', 'status', 'created_time', 'title', 'description', 'user', 'updated_time',
                  'admin_comment', 'messages']


class ClientTicketSerializer(serializers.ModelSerializer):
    """Сериализатор тикета для клиента"""
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Ticket
        fields = ['type', 'status', 'user', 'created_time', 'title', 'description', 'updated_time']


class MyUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор регистрации"""

    def validate_email(self, email):
        """Добавляем валидацию email, делая поле обязательным"""
        validate_email(email)
        return email
