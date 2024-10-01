from django import forms
from .models import Profile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']