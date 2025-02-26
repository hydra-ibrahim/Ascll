from django.urls import path
from .views import store_fcm_token, send_message

urlpatterns = [
    path('store_fcm_token/', store_fcm_token, name='store_fcm_token'),
    path('send_message/', send_message, name='send_message'),
]
