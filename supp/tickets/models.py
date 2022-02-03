from django.contrib.auth.models import User
from django.db import models
# статусы тикетов
from rest_framework.reverse import reverse

statuses = [
    ('В очереди', 'В очереди'),
    ('Принят в работу', 'Принят в работу'),
    ('Отвечен', 'Отвечен'),
    ('Вопрос решён', 'Вопрос решён')
]

# типы тикетов
types = [
    ('Финансы', 'Финансы'),
    ('Технические вопросы', 'Технические вопросы'),
    ('Жалобы и предложения', 'Жалобы и предложения'),
    ('Иные вопросы', 'Иные вопросы')
]


class Ticket(models.Model):
    """Модель тикета"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField('Статус', choices=statuses, max_length=150, default='queue')
    type = models.TextField('Тип запроса', choices=types, max_length=150)
    title = models.CharField('Тема', max_length=250)
    description = models.TextField('Описание проблемы', max_length=900)
    created_time = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_time = models.DateTimeField('Последнее обновление', auto_now=True)
    admin_comment = models.TextField('Комментарий администрации', max_length=500, blank=True)

    def get_tickets_messages(self):
        """Получение всех сообщений тикета"""
        return Message.objects.filter(ticket_id=self.pk).order_by('created_time')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_ticket', kwargs={'pk': self.pk})


class Message(models.Model):
    """Модель сообщения"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.TextField('Сообщение', max_length=900)
    created_time = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.text
