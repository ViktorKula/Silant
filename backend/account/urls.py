from django.urls import path
from allauth.account.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
]