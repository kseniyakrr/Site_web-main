import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
User = get_user_model()

class LoginUserForm(AuthenticationForm):

    username = forms.CharField(label='Логин',
    widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
    widget=forms.PasswordInput(attrs={'class': 'forminput'}))

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'forminput'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'forminput'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name','last_name', 'password1', 'password2']
        labels = {
                    'email': 'E-mail',
                    'first_name': 'Имя',
                    'last_name': 'Фамилия',
                }
        widgets = {
                    'email': forms.TextInput(attrs={'class':'form-input'}),
                    'first_name': forms.TextInput(attrs={'class': 'form-input'}),
                    'last_name': forms.TextInput(attrs={'class': 'form-input'}),
                }
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='Email', widget=forms.TextInput(attrs={'class': 'forminput'}))
    this_year = datetime.date.today().year 
    date_birth = forms.DateField(label = 'Дата рождения', widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'date_birth']
        labels = {
                    'first_name': 'Имя',
                    'last_name': 'Фамилия',
                    'date_birth': 'Дата рождения'
                }
        widgets = {
                'first_name':
                forms.TextInput(attrs={'class': 'form-input'}),
                'last_name':
                forms.TextInput(attrs={'class': 'form-input'}),
                }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'forminput'}))