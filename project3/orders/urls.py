from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("add/<str:item_type>/<str:item_id>/<str:size>", views.add, name="add"),
    path("delete_item/<str:item_type>/<str:item_id>", views.delete_item, name="delete_item"),
    path("delete_order", views.delete_order, name="delete_order"),
    path("submit_order", views.submit_order, name="submit_order"),
    path("orders", views.orders, name="orders")
]
