from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'autocomplete': 'off'}
        self.fields['email'].widget.attrs = {'autocomplete': 'off'}

    class Meta:
        model = User
        fields = [
            "username",
            "email", 
            "password1", 
            "password2"
        ]

class LoginForm(AuthenticationForm):
    username = UsernameField(
        required=True,
        widget=forms.TextInput(
            attrs={
                    'autofocus': True,
                    'class': 'form-control',
                    'placeholder': 'User name'
                }
        )
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'id': 'inputPassword',
                'class': 'form-control',
                'placeholder': 'Password',
            }
        ),
    )