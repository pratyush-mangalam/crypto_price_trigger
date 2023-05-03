import asyncio
import json

import websockets

from crypto_price_trigger.alert.models import Alert
from crypto_price_trigger.alert.tasks import send_email_task
from crypto_price_trigger.utils.redis_operation import get_alert_from_redis, delete_alert_from_redis

event_loop = asyncio.new_event_loop()


async def binance_websocket_api(email, symbol, set_price, alert_id):
    """
    The binance_websocket_api function is a coroutine that connects to the Binance websocket API and listens for price
    updates.
    When it receives an update, it compares the current price with the set_price. If they are equal, then we trigger
    our desired action (such as sending an email notification).

    :param email: Get the alert from redis
    :param symbol: Determine which symbol to monitor
    :param set_price: Set the price at which we want to trigger an action
    :param alert_id: Uniquely identify the alert
    :return: A coroutine object
    """
    uri = f'wss://stream.binance.com:9443/ws/{symbol}@kline_1m'

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            symbol = data['s']
            current_price = int(float(data['k']['c']))

            if not get_alert_from_redis(email=email, symbol=symbol.lower(), alert_id=alert_id):
                await websocket.close()
                return

            # Compare the current price with the set price
            if current_price >= set_price:
                # Trigger the desired action, such as sending an email notification
                data = {
                    'email': email,
                    'symbol': symbol,
                    'current_price': current_price,
                    'set_price': set_price
                }
                send_email_task.delay(json.dumps(data))
                alert = Alert.objects.get(id=alert_id)
                alert.status = "Triggered"
                alert.save()
                delete_alert_from_redis(email=email, symbol=symbol.lower(), alert_id=alert_id)
                await websocket.close()
                return


def binance_websocket_api_handler(email, symbol, price, alert_id):
    """
    The binance_websocket_api_handler function is a wrapper function that allows the binance_websocket_api
        function to be run in a separate thread. This is necessary because the binance_websocket_api function
        runs an event loop, which blocks any other code from running until it completes. The binance_websocket_api
        handler takes four arguments: email, symbol, price and alert id.

    :param email: Send the alert to the user's email address
    :param symbol: Specify the symbol to be used in the websocket api
    :param price: Set the price alert
    :param alert_id: Identify the alert that is being triggered
    :return: The following:
    """
    # Set the event loop for the current thread
    asyncio.set_event_loop(event_loop)
    # Start the event loop and run the WebSocket API
    event_loop.run_until_complete(binance_websocket_api(email, symbol, price, alert_id))
