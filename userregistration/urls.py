from django.urls import path
from .views import register, search_users, login_view,logout_view,user_details

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path(r'^search_users/$', search_users, name='search_users'),
     path("user-details/<int:user_id>/",user_details,name="user_details")
]