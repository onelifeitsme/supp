from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic.base import ContextMixin
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tickets.models import Message, Ticket

from .serializers import (ClientTicketSerializer, MessageSerializer,
                          StuffTicketSerializer)
from .service import is_spamer
from rest_framework.generics import ListCreateAPIView
from .permissions import OnlyOwnObjects, IsNotSpamer


class TicketsAPIView(ContextMixin, ListCreateAPIView):
    """Представление всех тикетов"""
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            tickets_status = self.request.query_params.get("status", None)
            if tickets_status:
                """Если параметром передан статус, отдаём тикеты с этим статусом"""
                return Ticket.objects.filter(status=tickets_status)
            else:
                """Если параметром не передан статус, отдаём все тикеты"""
                return Ticket.objects.all()
            """Если юзер - клиент, отдаём только его тикеты"""
        return Ticket.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StuffTicketSerializer
        return ClientTicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleTicketAPIView(RetrieveUpdateAPIView):
    """Представление одного тикета"""
    permission_classes = (IsAuthenticated, OnlyOwnObjects)
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StuffTicketSerializer
        return ClientTicketSerializer

    @method_decorator(staff_member_required)
    def patch(self, *args, **kwargs):
        return self.partial_update(*args, **kwargs)


class TicketMessagesAPIView(ListCreateAPIView):
    """Представление сообщений конкретного тикета"""
    permission_classes = (IsAuthenticated, OnlyOwnObjects)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     return Message.objects.filter(ticket_id=self.kwargs['pk'])

    def post(self, request, pk):
        serializer = self.get_serializer_class(request)(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.validated_data['ticket_id'] = pk
            serializer.save()
            return Response({'Сообщение отправлено': serializer.data})
        return Response(serializer.errors)
