from django.urls import path

from crypto_price_trigger.users import views

urlpatterns = [
    path("signup/", views.UserSignUp.as_view(), name="signup"),
    path('login/', views.UserLogIn.as_view(), name='login'),

]
