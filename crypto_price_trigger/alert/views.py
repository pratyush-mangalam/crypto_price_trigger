import threading

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from crypto_price_trigger.alert.binance_wensocket import binance_websocket_api_handler
from crypto_price_trigger.alert.models import Alert
from crypto_price_trigger.alert.serializers import AlertSerializer, AlertListSerializer
from crypto_price_trigger.users.models import Users
from crypto_price_trigger.utils.custom_exception import PermissionDenied
from crypto_price_trigger.utils.redis_operation import set_alert_in_redis, delete_alert_from_redis


class CreateAlert(APIView):

    def post(self, request):
        """
        The post function creates a new alert for the user.
            The function takes in an email, stock_id, and stock_price as parameters.
            It then saves this data to the database and sets it in redis with set_alert_in_redis().
            Finally, it starts a thread that runs binance websocket api handler.

        :param self: Represent the instance of the object itself
        :param request: Get the data from the request
        :return: The data that was passed in the request
        :doc-author: Trelent
        """
        alert = AlertSerializer(data=request.data)
        alert.is_valid(raise_exception=True)
        alert.save()
        data = alert.validated_data
        set_alert_in_redis(email=data["email"], alert_id=data["id"], symbol=data["stock_id"], price=data["stock_price"])
        websocket_thread = threading.Thread(target=binance_websocket_api_handler, args=(data["email"], data["stock_id"],
                                                                                        data["stock_price"]))
        websocket_thread.start()
        return Response(data=data, status=status.HTTP_201_CREATED)


class DeleteAlert(APIView):

    def delete(self, request, alert_id):

        """
        The delete function is used to delete an alert.
            It takes in the request and the id of the alert that needs to be deleted.
            The function first checks if there exists an alert with that id, if not it returns a 404 error message.
            If there does exist such an alert, then it sets its deleted field to True and saves this change in the database.
            Then we call our helper function delete_alert_from_redis which deletes this particular email-symbol pair from redis.

        :param self: Represent the instance of the object itself
        :param request: Get the request object, which is an instance of httprequest
        :param alert_id: Identify the alert to be deleted
        :return: A 204 no content response
        :doc-author: Trelent
        """
        try:
            alert = Alert.objects.get(id=alert_id)
        except Alert.DoesNotExist:
            return Response({"error": "Alert not found"}, status=status.HTTP_404_NOT_FOUND)

        alert.deleted = True
        alert.save()
        data = alert.validated_data
        delete_alert_from_redis(email=data["email"], alert_id=data["id"], symbol=data["stock_id"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlertList(APIView):
    def get(self, request, user_id):

        """
        The get function is used to retrieve all alerts for a given user.
            The function takes in the request and user_id as parameters.
            It then checks if the user exists, if not it raises an error.
            If the status filter is present, it filters by that status otherwise
                it returns all alerts for that user.

        :param self: Represent the instance of the object itself
        :param request: Get the request object, which contains all the information about the current http request
        :param user_id: Filter the alerts by user
        :return: A list of alerts with the following fields:
        :doc-author: Trelent
        """
        status_filter = request.query_params.get('status')
        page_limit = request.query_params.get('page_limit')
        page = request.query_params.get('page')
        user = Users.objects.filter(id=user_id)
        if not user.exists():
            raise PermissionDenied(
                {"details": f"user {user_id} doesn't exists"}
            )
        if status_filter:
            alerts = Alert.objects.filter(status=status_filter, user=user)
        else:
            alerts = Alert.objects.filter(user=user)

        # Pagination
        paginator = PageNumberPagination()
        if page_limit:
            paginator.page_size = page_limit
        if page:
            paginator.page = page
        paginated_alerts = paginator.paginate_queryset(alerts, request)
        serializer = AlertListSerializer(paginated_alerts, many=True)

        # Include status in response
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
