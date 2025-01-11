from django.urls import path, include
from .views import quest_and_answer,receive_user_answer,send_massage

app_name = "MENTES"
urlpatterns = [
    path('questions/',quest_and_answer,name='question')
   ,path('user-answers/',receive_user_answer,name='answers'),
   path('send-email/',send_massage,name='send_email')

]
