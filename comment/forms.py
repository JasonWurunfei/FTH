from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()


    class Meta:
        model = Comment
        fields = '__all__'