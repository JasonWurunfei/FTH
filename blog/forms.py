from django import forms
from django.forms import ModelForm
from .models import BlogPost
from markdownx.widgets import MarkdownxWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

MarkdownxWidget.template_name = 'markdownx/widget2.html'

class BlogForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'body',
            'created_date',
            'mod_date',
             Submit('submit', 'Submit', css_class='btn btn-primary btn-lg'),
        )
        self.fields['body'].label = ''
        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['mod_date'].widget = forms.HiddenInput()
        self.fields['body'].widget = MarkdownxWidget(
            attrs={
                'style': '''
                        background-color:#ffffe6;
                        min-width:500px;
                        min-height:500px;
                ''',
            }
        )

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'created_date', 'mod_date']
