from django import forms
from keptar.models import PBlogEntry

class PBlogEntryForm(forms.ModelForm):
    class Meta:
        model = PBlogEntry
        exclude = ('user')
        widgets = {
                'path': forms.HiddenInput(),
                }
