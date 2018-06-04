from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.PasswordInput()


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=15, required=True,
                               widget=forms.TextInput(attrs={'class': 'uk-input uk-margin-small-bottom'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-margin-small-bottom'}),
                               required=True)
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'uk-input uk-margin-small-bottom'}),
                                      required=True)
    describe_yourself = forms.CharField(required=False, max_length=240,
                                        widget=forms.Textarea(attrs={'class': 'uk-input uk-margin-small-bottom'}))
    gender = forms.ChoiceField(choices=(('Male', 'Male'),
                                        ('Female', 'Female'),
                                        ))
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=[i + 1 for i in range(1909, 2018)],
                                                               attrs={'class': 'uk-margin-small-bottom'}))
    email = forms.EmailField(widget=forms.HiddenInput)
