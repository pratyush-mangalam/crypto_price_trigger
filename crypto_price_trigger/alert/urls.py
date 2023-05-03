from django.urls import path

from crypto_price_trigger.alert import views

urlpatterns = [
    path("create_alert/", views.CreateAlert.as_view(), name="create alert"),
    path("delete_alert/<int:alert_id>/", views.DeleteAlert.as_view(), name="delete alert"),
    path("get_alerts/user/<int:user_id>/", views.AlertList.as_view(), name="get alert"),

]
