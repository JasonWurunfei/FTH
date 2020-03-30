from django import forms
from django.forms import ModelForm
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
# from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs = {'autocomplete': 'off'}
#         self.fields['email'].widget.attrs = {'autocomplete': 'off'}

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "email", 
#             "password1", 
#             "password2"
#         ]

# class LoginForm(AuthenticationForm):
#     username = UsernameField(
#         required=True,
#         widget=forms.TextInput(
#             attrs={
#                     'autofocus': True,
#                     'class': 'form-control',
#                     'placeholder': 'User name'
#                 }
#         )
#     )
#     password = forms.CharField(
#         label="Password",
#         strip=False,
#         required=True,
#         widget=forms.PasswordInput(
#             attrs={
#                 'autocomplete': 'current-password',
#                 'id': 'inputPassword',
#                 'class': 'form-control',
#                 'placeholder': 'Password',
#             }
#         ),
#     )

class UserProfileEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                'date_of_birth',
                'major',
                'class_num',
            ),
            'bio',
            Row(
                'profile_pic'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary btn-lg')
        )

    class Meta:
        model = User
        fields = ['date_of_birth', 'major', 'class_num', 'bio', 'profile_pic',]
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
