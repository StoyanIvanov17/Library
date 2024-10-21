from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from library.lb_accounts.models import LibraryProfile

UserModel = get_user_model()


class LibraryUserCreationForm(auth_forms.UserCreationForm):
    usable_password = None
    user = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', )


class LibraryChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel


class LibraryProfileForm(forms.ModelForm):
    class Meta:
        model = LibraryProfile
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'city', 'profile_picture']

        widgets = {
            'profile_picture': forms.FileInput(attrs={'placeholder': 'Profile Picture'}),
        }