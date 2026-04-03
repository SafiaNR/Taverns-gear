from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import User

class CyrillicValidator:
    def __call__(self, value):
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', value):
            raise ValidationError('Разрешены только кириллица, пробел и дефис')

class CustomUserCreationForm(UserCreationForm):
    
    first_name = forms.CharField(
        label='Имя',
        max_length=150,
        required=True,
        validators=[CyrillicValidator()],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=150,
        required=True,
        validators=[CyrillicValidator()],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Петров'})
    )
    patronymic = forms.CharField(
        label='Отчество',
        max_length=150,
        required=False,
        validators=[CyrillicValidator()],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванович'})
    )
    username = forms.CharField(
        label='Логин',
        max_length=150,
        required=True,
        help_text='Только латиница, цифры и дефис',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ivan_petrov'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@example.com'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}),
        help_text='Пароль должен содержать не менее 6 символов'
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'})
    )
    agreement = forms.BooleanField(
        label='Согласие с правилами регистрации',
        required=True,
        error_messages={'required': 'Необходимо согласиться с правилами'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9\-]+$', username):
            raise ValidationError('Разрешены только латиница, цифры и дефис')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 6:
                raise ValidationError('Пароль должен содержать не менее 6 символов')
        return password

class CustomAuthenticationForm(AuthenticationForm):
    
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    
    error_messages = {
        'invalid_login': 'Неверный логин или пароль',
        'inactive': 'Учетная запись неактивна',
    }
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].error_messages = {}
        self.fields['password'].error_messages = {}