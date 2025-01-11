from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request=request,template_name='home.html')

def render_get_test(request):
    return render(request=request,template_name='GetTest.html')

def doctors_list(request):
    return render(request=request,template_name='Doctors.html')

def about(request):
    return render(request=request,template_name='about.html')