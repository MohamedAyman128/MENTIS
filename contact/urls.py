from django.urls import path, re_path
from .views import contact

app_name = 'contact'

urlpatterns = [
    path('', contact, name='contact'),
    
]