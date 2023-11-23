from django.urls import path
from . import views

app_name = "papers"
urlpatterns = [
    path('createPaper', views.createPaper, name="createPaper"),
    path('<int:paper_uid>', views.loadPaper, name="loadPaper"),
]
