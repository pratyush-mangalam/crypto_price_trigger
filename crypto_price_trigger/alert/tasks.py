import json

from celery import shared_task

from crypto_price_trigger.utils.email_handler import send_email_notification


@shared_task
def send_email_task(request):
    """
    The send_email_task function is a Celery task that sends an email notification to the user when the price of a stock
    they are tracking reaches or falls below their set price. The function takes in JSON data from the frontend,
    which includes:

    :param request: Get the data from the post request
    :return: None
    """
    data = json.loads(request)
    send_email_notification(data["email"], data["symbol"], data["current_price"], data["set_price"])
    return None
