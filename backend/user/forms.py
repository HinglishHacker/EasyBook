from django import forms
from .models import Passenger
import re

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = Passenger
        fields = ['email', 'first_name', 'last_name', 'phone', 'passport_number', 'avatar']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def clean_passport_number(self):
        passport = self.cleaned_data.get("passport_number")
        pattern = r"^\d{4}\s\d{6}$"
        if not re.match(pattern, passport):
            raise forms.ValidationError("Введите паспорт в формате: 1234 567890")
        digits = passport.replace(" ", "")
        if len(set(digits)) == 1:
            raise forms.ValidationError("Недопустимый номер паспорта")
        return passport

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
