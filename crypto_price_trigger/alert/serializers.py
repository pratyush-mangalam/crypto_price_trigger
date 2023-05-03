from rest_framework import serializers

from crypto_price_trigger.alert.models import Alert
from crypto_price_trigger.users.models import Users


class AlertSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Alert
        fields = ['id', 'stock_id', 'stock_name', 'stock_price', 'email', 'alert_sent', 'created_date']

    def create(self, validated_data):
        email = validated_data.pop('email')
        user = Users.objects.get(email=email)
        validated_data["user"] = user
        alert = Alert.objects.create(**validated_data)
        return alert


class AlertListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'stock_id', 'stock_name', 'stock_price', 'alert_sent', 'status', 'created_date']
