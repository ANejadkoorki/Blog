from django import forms


class LoginForm(forms.Form):
    """
    the login form
    """
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
