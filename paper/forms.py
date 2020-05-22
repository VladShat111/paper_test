from django import forms


class TokenRetrieveForm(forms.Form):
    grant_type = forms.CharField(max_length=120,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'grant_type'}))
    username = forms.CharField(max_length=120,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}))
    password = forms.CharField(max_length=120,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'password'}))
    client_id = forms.CharField(max_length=120,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'client_id'}))
    client_secret = forms.CharField(max_length=120,
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'client_secret'}))
