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
    if queryset:
        messages_queryset_to_list = [message for message in queryset]
        if len(messages_queryset_to_list) > 2:
            last_3_messages = messages_queryset_to_list[-3:]
            if (last_3_messages[0].user.is_staff is False
                    and last_3_messages[1].user.is_staff is False
                    and last_3_messages[2].user.is_staff is False):
                return True
    return False
