from django.urls import path, re_path
from .views import home, render_get_test,doctors_list, about

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('GetTest/', render_get_test, name='GetTest'),
    path('Doctors/', doctors_list, name='Doctors'),
    path('about/', about, name='about'),
]