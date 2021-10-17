from django import forms

class ProfileEditForm(forms.Form):
    username = forms.CharField(min_length=5, required=False)
    email = forms.CharField(min_length=10, required=False, widget=forms.EmailInput)
    nickname = forms.CharField(min_length=5, required=False)
    avatar = forms.ImageField(required=False)


class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, required=True)
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(min_length=5, required=True)
    email = forms.CharField(min_length=10, required=True, widget=forms.EmailInput)
    nickname = forms.CharField(min_length=5, required=True)
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)
    reapeat = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)
