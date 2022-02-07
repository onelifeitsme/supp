from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.core.validators import validate_email
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.settings import api_settings
from tickets.models import Message, Ticket


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщения"""
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Message
        fields = ('created_time', 'user', 'text')


class StuffTicketSerializer(serializers.ModelSerializer):
    """Сериализатор тикета для персонала"""
    user = serializers.CharField(source='user.username', read_only=True)
    messages = MessageSerializer(source='get_tickets_messages', many=True, required=False)

    class Meta:
        model = Ticket
        fields = ('type', 'status', 'created_time', 'title', 'description', 'user', 'updated_time',
                  'admin_comment', 'messages')


class ClientTicketSerializer(serializers.ModelSerializer):
    """Сериализатор тикета для клиента"""
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Ticket
        fields = ('type', 'status', 'user', 'created_time', 'title', 'description', 'updated_time')


class MyUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор регистрации"""
    email = serializers.EmailField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
            'email',
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        email = attrs.get('email')
        try:
            validate_password(password, user)
            validate_email(email)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]})
        return attrs
