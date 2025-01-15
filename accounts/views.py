from typing import Any
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Profile
from .forms import ProfileForm, SingUpForm, UserForm
from django.views.generic import TemplateView
from django.db import transaction


class SignUpView(CreateView):
    form_class = SingUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/sign-up.html"
    
    @transaction.atomic
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        age = form.cleaned_data.get('age')
        gender = form.cleaned_data.get('gender')
        if self.object: 
           profile = Profile.objects.create(user=self.object)
           profile.age = age
           profile.gender = gender
           profile.save()  
           
        return response

class ShowProfileView(TemplateView):
    template_name = "registration/profile.html"
    
    def get_context_data(self, **kwargs:Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user) 
        context["profile"] = profile 
        return context
    

class ProfileUpdateView(UpdateView):
    template_name = "registration/edit_profile.html"
    form_class = ProfileForm
    success_url = '../profile/'
    
    def get_object(self):
        obj = Profile.objects.get(user=self.request.user)  
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)  # بيانات المستخدم المحدّثة
        context['profile_form'] = self.form_class(instance=self.get_object())  # بيانات الملف الشخصي المحدّثة
        return context


    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)  
        if user_form.is_valid():
            user_form.save()
            self.request.user.refresh_from_db()  # تحديث بيانات المستخدم
        response = super().form_valid(form)
        self.object.refresh_from_db()  # تحديث بيانات الملف الشخصي
        return response

