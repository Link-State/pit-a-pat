from django.urls import path
from . import views

app_name = 'message'
urlpatterns = [
    path('createMessage', views.createMessage, name='createMessage'),
]
