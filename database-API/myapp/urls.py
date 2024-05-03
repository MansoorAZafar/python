# app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_comment/', views.add_comment, name='add_comment'),
    path('get_comments/', views.get_comments, name='get_comments'),
    path('get_available_locations/', views.get_available_locations, name='get_available_locations'),
    path('slot_type/', views.slot_type, name='slot_type'),
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    path('add_user/', views.add_user, name="add_user"),
    path('remove_reservation/', views.remove_reservation, name='remove_reservation'),
    path('get_your_reservations/', views.get_your_reservations, name='get_your_reservations'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('add_default_data/', views.add_default_data, name='add_default_data'),
]
