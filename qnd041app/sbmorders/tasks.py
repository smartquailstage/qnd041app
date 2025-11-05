from qnd041app.celery import app
from django.core.mail import send_mail
from .models import Order

@app.task(bind=True)
def order_created(self, order_id):
    """
    Task to send an e-mail notification when an order is 
    successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist
        self.retry(countdown=60, max_retries=3)
    
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\nYour order id is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(
        subject,
        message,
        'info@mail.smartquail.io',
        [order.email],
        fail_silently=False
    )
    return mail_sent

@app.task(bind=True)
def generate_pdf_and_send_email(order_id, bank_transfer_id):
    """
    Task to send an e-mail notification when an order is 
    successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist
        self.retry(countdown=60, max_retries=3)
    
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\nYour order id is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(
        subject,
        message,
        'info@mail.smartquail.io',
        [order.email],
        fail_silently=False
    )
    return mail_sent