from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags
from .models import Ribbit


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def is_valid(self):
        form = super().is_valid()
        for f, error in self.errors.items():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        model = User


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super().is_valid()
        for f, error in self.errors.items():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form


class RibbitForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'ribbitText'}))

    def is_valid(self):
        form = super().is_valid()
        for f, error in self.errors.items():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error ribbitText'})
        return form

    class Meta:
        model = Ribbit
        exclude = ('user',)
