from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("error/", views.error, name = "error"),
    path("login/", views.login, name = "login"),
    path("signup/", views.signup, name = "signup"),
    path("account/<int:Customer_id>/", views.account, name = "account"),
    path("deposit/<int:Customer_id>/", views.deposit, name = "deposit"),
    path("transfer/<int:Customer_id>/", views.transfer, name = "transfer"),
    path("manager/<int:Customer_id>/", views.manager, name = "manager"),
    path("logout/", views.logout, name = "logout"),
]