from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Enter your Username', max_length=40)
