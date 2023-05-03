from django.conf import settings
from django.core.mail import get_connection, EmailMessage


def send_email_notification(email, symbol, current_price, set_price):
    """
    The send_email_notification function sends an email to the user when a stock price reaches their set price.
        Args:
            email (str): The user's email address.
            symbol (str): The stock symbol for which the notification is being sent.
            current_price (float): The current price of the stock at time of notification.  This will be compared to
                set_price in order to determine whether a notification should be sent out, and if so, what
                message should be included in that notification.

    :param email: Send the email to a specific user
    :param symbol: Get the stock symbol
    :param current_price: Get the current price of the stock
    :param set_price: Set the price for which we want to get notified
    :return: A boolean value
    """
    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        recipient_list = [email]
        subject = "Stock price reached at you set price"
        email_from = settings.EMAIL_HOST_USER
        message = f'Hi, Your {symbol} current price {current_price} is reached at your set price {set_price}'
        EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
