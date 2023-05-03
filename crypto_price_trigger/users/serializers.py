from django.conf import settings
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from crypto_price_trigger.authentication.jwt import generate_jwt_token
from crypto_price_trigger.users.models import Users

hasher = PBKDF2PasswordHasher()
salt = settings.SALT


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("id", "name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Users.objects.create(**validated_data)

    def validate_email(self, value):  # noqa

        """
        The validate_email function checks if the email already exists in the database.
        If it does, then a ValidationError is raised with a message that says &quot;user &lt;username&gt; already exists&quot;.


        :param self: Pass the instance of the model to be validated
        :param value: Pass in the email address that is being validated
        :return: The value of the email field
        :doc-author: Trelent
        """
        email = Users.objects.filter(email=value)
        if email.exists():
            duplicate_obj = Users.objects.get(email=email)
            raise ValidationError(
                {"details": f"user {duplicate_obj.user} already exists"}
            )
        return value

    def validate_password(self, val):
        """
        The validate_password function takes a password as an argument and returns the hashed version of that password.
        The function uses the encode method from the passlib library to hash passwords using sha256_crypt.

        :param self: Refer to the object itself
        :param val: Pass in the password that is being validated
        :return: The hashed password
        :doc-author: Trelent
        """
        password = val.encode("utf-8")
        hashed_password = hasher.encode(password, salt)
        return hashed_password


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):

        """
        The validate function is used to validate the data that is passed in by the user.
            It checks if a user exists with the email provided and then it checks if
            password matches with that of stored in database. If both conditions are met,
            it returns a token which can be used for further authentication.

        :param self: Represent the instance of the class
        :param attrs: Pass the data that is sent in the request body
        :return: The user object with the token
        :doc-author: Trelent
        """
        email = Users.objects.filter(email=attrs["email"], active=True)

        if not email.exists():
            raise PermissionDenied(
                {"details": f"user {attrs['email']} doesn't exists"}
            )
        hashed_password = hasher.encode(attrs["password"], salt)
        user = Users.objects.filter(email=attrs["email"], password=hashed_password).values(
            "id", "name", "email")
        if not user.exists():
            raise PermissionDenied({"details": "Incorrect Password"})
        user = list(user)[0]
        token = generate_jwt_token(user)
        user.update({"token": token})
        return user
