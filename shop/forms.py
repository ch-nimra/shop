from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)\

class SearchForm(forms.Form):
    query = forms.CharField()