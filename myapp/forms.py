from django import forms
from myapp.models import *
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'last_name', 'passport_number', 'email', 'phone_number']
