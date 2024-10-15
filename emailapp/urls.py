from . import views
from django.urls import path

app_name = 'emailapp'

urlpatterns = [
    path('', views.home, name="home"),
]