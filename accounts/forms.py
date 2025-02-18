from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    pet_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Change field name to pet_name

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'pet_name')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Ensure the profile is created only if it does not exist
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'pet_name': self.cleaned_data['pet_name']  # Change field name to pet_name
                }
            )
        return user