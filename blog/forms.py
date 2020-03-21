from django import forms
from django.forms import ModelForm
from .models import BlogPost, BlogSeries
from markdownx.widgets import MarkdownxWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

MarkdownxWidget.template_name = 'markdownx/widget2.html'

class BlogForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user',
            'title',
            'body',
            'created_date',
            'mod_date',
             Submit('submit', 'Submit', css_class='btn btn-primary btn-lg'),
        )
        self.fields['title'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        self.fields['body'].label = ''
        self.fields['user'].widget = forms.HiddenInput()
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
        fields = ['user', 'title', 'body', 'created_date', 'mod_date']


class BlogModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "blog title: %s" % obj.title

class SeriesForm(ModelForm):

    blogs = BlogModelMultipleChoiceField(
        queryset=BlogPost.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        to_field_name="id"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['title'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        
        self.fields['description'].widget = forms.Textarea()
        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['mod_date'].widget = forms.HiddenInput()
        self.fields['blogs'].queryset = BlogPost.objects.filter(user=user)
        self.fields['blogs'].to_field_name = "title"
        
    class Meta:
        model = BlogSeries
        fields = ['user', 'title', 'description', 'background_image', 'created_date', 'mod_date']
