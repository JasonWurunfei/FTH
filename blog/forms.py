from django import forms
from django.forms import ModelForm
from .models import BlogPost
from markdownx.widgets import MarkdownxWidget

MarkdownxWidget.template_name = 'markdownx/widget2.html'

class BlogForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['body'].label = ''
        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['mod_date'].widget = forms.HiddenInput()

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'created_date', 'mod_date']