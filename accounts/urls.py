from django.urls import path
from .views import SignUpView , ShowProfileView, ProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path("auth/", SignUpView.as_view(), name="signup"),
    path('profile/', ShowProfileView.as_view(), name='profile'),
    path('edit-profile/', ProfileUpdateView.as_view(), name='edit-profile')
]