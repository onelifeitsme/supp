from django.core.mail import send_mail


def send_about_new_ticket_status(user_email, new_status):
    """Функция отправки письма об изменении статуса тикета создателю тикета"""
    send_mail(
        'Статус вашего тикета изменён',
        f'Статус вашего тикета: {new_status}',
        'mytestmail090009@gmail.com',
        [user_email],
        fail_silently=False
    )


def is_spamer(queryset):
    """Функция проверяет, являются ли последние три сообщения в тикете сообщениями клиента"""
    if len(queryset) > 2:
        last_3_messages = [message for message in queryset][-3:]
        return all([(message.user.is_staff is False) for message in last_3_messages])
    return False
