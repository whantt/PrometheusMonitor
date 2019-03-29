from django import forms


class Forms(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
