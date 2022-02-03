from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tickets.models import Message, Ticket

from .serializers import (ClientTicketSerializer, MessageSerializer,
                          StuffTicketSerializer)
from .service import is_spamer
from .tasks import task_send_about_new_ticket_status


class TicketsAPIView(APIView):
    """Представление всех тикетов"""
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, request):
        if request.user.is_staff is True:
            tickets_status = self.request.query_params.get("status", None)
            if tickets_status:
                """Если параметром передан статус, отдаём тикеты с этим статусом"""
                return Ticket.objects.filter(status=tickets_status)
            else:
                """Если параметром не передан статус, отдаём все тикеты"""
                return Ticket.objects.all()
            """Если юзер - клиент, отдаём только его тикеты"""
        return Ticket.objects.filter(user=request.user)

    def get_serializer_class(self, request):
        if request.user.is_staff is True:
            return StuffTicketSerializer
        return ClientTicketSerializer

    def get(self, request):
        tickets = self.get_queryset(request)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(tickets, request)
        serializer = self.get_serializer_class(request)(result_page, many=True)
        return Response({'tickets': serializer.data})

    def post(self, request):
        serializer = self.get_serializer_class(request)(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'Новый тикет успешно создан': serializer.data})
        return Response(serializer.errors)


class SingleTicketAPIView(APIView):
    """Представление одного тикета"""
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, request, pk):
        if request.user.is_staff is True:
            return get_object_or_404(Ticket, pk=pk)
        else:
            return get_object_or_404(Ticket, user=request.user, pk=pk)

    def get_serializer_class(self, request):
        if request.user.is_staff is True:
            return StuffTicketSerializer
        return ClientTicketSerializer

    def get(self, request, pk):
        serializer = self.get_serializer_class(request)(self.get_queryset(request, pk))
        return Response({'ticket': serializer.data})

    def patch(self, request, pk):
        if request.user.is_staff is True:
            serializer = self.get_serializer_class(request)(self.get_queryset(request, pk),
                                                            data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if 'status' in serializer.validated_data:
                    """Если изменяется статус тикета, то отправляется письмо на почту создателю тикета"""
                    user_email = self.get_queryset(request, pk).user.email
                    new_status = serializer.validated_data['status']
                    task_send_about_new_ticket_status.delay(user_email, new_status)
                return Response({'Тикет обновлён': serializer.data})
            return Response(serializer.errors)


class TicketMessagesAPIView(APIView):
    """Представление сообщений конкретного тикета"""
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, request, pk):
        request_ticket = Ticket.objects.get(pk=pk)
        if request.user.is_staff is True or request_ticket.user == request.user:
            """Если юзер - сотрудник или запрашиваемый тикет ялвяется тикетом юзера"""
            return Message.objects.filter(ticket_id=pk)
        else:
            return None

    def get_serializer_class(self, request):
        return MessageSerializer

    def get(self, request, pk):
        serializer = self.get_serializer_class(request)(self.get_queryset(request, pk), many=True)
        return Response({'Сообщения тикета': serializer.data})

    def post(self, request, pk):
        if is_spamer(self.get_queryset(request, pk)) is True and request.user.is_staff is False:
            """Если больше 3 сообщений подряд и юзер не сотрудник"""
            return Response('Дождитесь ответа от администрации')
        else:
            serializer = self.get_serializer_class(request)(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = request.user
                serializer.validated_data['ticket_id'] = pk
                serializer.save()
                return Response({'Сообщение отправлено': serializer.data})
            return Response(serializer.errors)
