from supp.celery import app

from .service import send_about_new_ticket_status


@app.task
def task_send_about_new_ticket_status(user_email, new_status):
    send_about_new_ticket_status(user_email, new_status)
