
from django.urls import path
from .views import LoginView, RegisterView, GuestRegisterView
from django.contrib.auth.views import LogoutView

app_name = "account"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('guest/', GuestRegisterView.as_view(), name="guest"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
]