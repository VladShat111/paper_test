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


class SearchForm(forms.Form):

    seria = forms.CharField(max_length=10,
                                 required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'seria',
                                                               'placeholder': '2МДО'}))

    number = forms.CharField(max_length=50,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'number',
                                                               'placeholder': '974847'}))
