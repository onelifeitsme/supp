from django.urls import path

from .views import SingleTicketAPIView, TicketMessagesAPIView, TicketsAPIView

urlpatterns = [
    path('tickets/', TicketsAPIView.as_view(), name='tickets'),
    path('ticket/<int:pk>', SingleTicketAPIView.as_view(), name='single_ticket'),
    path('ticket/<int:pk>/messages', TicketMessagesAPIView.as_view(), name='ticket_messages')
]
