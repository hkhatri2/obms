from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="librarian/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change_done/", auth_views.PasswordChangeDoneView.as_view(template_name="librarian/password_change_done.html"), name="password_change_done"),
    path("create_new_user/", views.create_new_user, name="create_new_user"),
    path("librarian/", views.librarian, name="librarian"),
    path("profile/", views.profile, name="profile"),
    path("cart/", views.cart, name="cart"),
    
    path("books", views.books, name="books"),
    path("readers", views.readers, name="readers"),
    path("cart_api", views.cart_api, name="cart_api"),
]