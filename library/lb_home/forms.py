from django import forms

from library.lb_home.models import BestAuthors


class BestAuthorsCreateForm(forms.ModelForm):
    class Meta:
        model = BestAuthors
        fields = ['name', 'author_image']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'author_image': forms.FileInput(attrs={'placeholder': 'Author Image'}),
        }