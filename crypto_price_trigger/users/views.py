from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crypto_price_trigger.users.serializers import UserSignUpSerializer, UserLoginSerializer


class UserSignUp(APIView):
    authentication_classes = []

    def post(self, request):
        """
        The post function creates a new user.
            It takes in the request data and validates it using the UserSignUpSerializer.
            If validation is successful, it saves the validated data to create a new user object.
            The function then returns a response with an appropriate message and status code.

        :param self: Represent the instance of the class
        :param request: Get the data from the user
        :return: A response object with a message and status code
        """
        user = UserSignUpSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user = user.save()
        data = {
            "message": f"User created successfully. for '{user.email}' "
                       f"please login."
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class UserLogIn(APIView):
    authentication_classes = []

    def post(self, request):
        """
        The post function is used to log in a user.
            It takes the username and password as parameters, and returns a token if the login was successful.

        :param self: Represent the instance of the object itself
        :param request: Get the data from the client
        :return: A response object
        """
        ser = UserLoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        return Response(data, status=status.HTTP_200_OK)
