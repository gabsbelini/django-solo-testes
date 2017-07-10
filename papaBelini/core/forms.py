from django import forms


class GraphForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
