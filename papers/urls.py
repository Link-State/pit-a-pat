from django.urls import path
from . import views

app_name = "papers"
urlpatterns = [
    path('createPaper', views.createPaper, name="createPaper"),
]
