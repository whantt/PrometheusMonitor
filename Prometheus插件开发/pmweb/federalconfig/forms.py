from django import forms


class Forms(forms.Form):
    fname = forms.CharField()
    furl = forms.CharField()


class Dforms(forms.Form):
    fid = forms.CharField()