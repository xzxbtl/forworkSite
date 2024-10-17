from . import views
from django.urls import path

app_name = 'emailapp'

urlpatterns = [
    path('', views.home, name="home"),
    path('mailadd/', views.add_mail, name='mailadd')
]