from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'trn_number', 'company_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\"../password/\" >'
                                                   'this form <a/>.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'trn_number', 'company_name', 'is_active', 'is_admin',
                  'is_superuser', 'last_login']
