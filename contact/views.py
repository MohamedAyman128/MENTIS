import http
import json
from django.shortcuts import render
from .models import Contact
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def contact(request):
    if request.method == 'POST':
        name = request.user.username
        email = "no email found " if not request.user.email else request.user.email
        message = request.POST['message']
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        return render(request, 'sucess_contact.html')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
