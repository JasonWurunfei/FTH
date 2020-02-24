from django import forms
from markdownx.fields import MarkdownxFormField

class BlogForm(forms.Form):
    myfield = MarkdownxFormField(label='')
    myfield.widget.template_name = 'markdownx/widget2.html'