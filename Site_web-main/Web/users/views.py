from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import LoginUserForm, ProfileUserForm, RegisterUserForm, User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from .forms import UserPasswordChangeForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

# Create your views here.

""" def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('homepage'))
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form}) """

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}
    
   


""" def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login')) """

class LogoutUser(LogoutView):
    form_class = AuthenticationForm
    extra_context = {'title': 'Выход из системы'}
    template_name = 'users/login.html'



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'date_birth']  # Все поля, которые нужно редактировать
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')  # Перенаправление после успешного сохранения
    
    def get_object(self):
        return self.request.user  # Работаем с текущим пользователем
    
    def form_valid(self, form):
        # Дополнительная обработка перед сохранением
        return super().form_valid(form)



class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}


class CustomPasswordResetView(PasswordResetView):
    """Кастомное представление для сброса пароля"""
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Сообщение об отправке письма"""
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Подтверждение сброса пароля"""
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Сообщение об успешном сбросе пароля"""
    template_name = 'users/password_reset_complete.html'

    