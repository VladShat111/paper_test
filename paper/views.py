# Create your views here.
from functools import wraps
from django.shortcuts import render
import requests
from datetime import datetime
from .forms import TokenRetrieveForm, SearchForm
from django.contrib import messages
from django.shortcuts import reverse, redirect
from .models import Person
# Create your views here.


def token_exp(something):
    @wraps(something)
    def wrap(*args, **kwargs):

        req = args[0]
        if datetime.now().timestamp() > req.session['expires_in']:
            print(f"current time: {datetime.now().timestamp()}, token time : {req.session['expires_in']}")
            return redirect(token_exp)
        return something(*args, **kwargs)
    return wrap


def get_token(request):

    if request.method == 'POST':

        form = TokenRetrieveForm(request.POST)

        if form.is_valid():
            dat = {'grant_type': form.cleaned_data['grant_type'],
                    'username': form.cleaned_data['username'],
                   'password': form.cleaned_data['password']}

            client_id = form.cleaned_data['client_id']
            client_secret = form.cleaned_data['client_secret']

            try:
                token = requests.post('http://mainapi.hsc.gov.ua/auth-server/oauth/token', data=dat,
                                  auth=(client_id, client_secret)).json()
            except Exception as e:
                print(e)
                messages.warning(request, 'Пароль пароль або логін невірний.')
                return redirect(get_token)

            try:
                request.session['token'] = 'Bearer ' + token['access_token']
                request.session['expires_in'] = token['expires_in'] + datetime.now().timestamp()
            except KeyError as err:
                messages.warning(request, 'Пароль пароль або логін невірний.')
                return redirect(get_token)

            except IndexError as err:
                messages.warning(request, 'Пароль пароль або логін невірний.')
                return redirect(get_token)

            messages.success(request, 'Доступ до пошуку дозволений.')
            return redirect(search_doc)

    else:
        form = TokenRetrieveForm()

    return render(request, 'app/paper/token_retrieve.html', {'form': form})


@token_exp
def search_doc(request):
    if request.method == 'POST':
        header = {'Authorization': request.session['token']}

        form = SearchForm(request.POST)

        if form.is_valid():

            seria = form.cleaned_data['seria']
            number = form.cleaned_data['number']

            doc = requests.get(f"http://mainapi.hsc.gov.ua/test-service/document/med?seria={seria}&number={number}",
                               headers=header).json()
            try:
                context = {'doc_type': doc['body'][0]['typeDoc']['typeDoc'],
                'doc_type_id': doc['body'][0]['typeDoc']['typeDocId'],
                'doc_status': doc['body'][0]['typeDoc']['status'],
                'doc_seria': doc['body'][0]['seria'],
                'doc_number': doc['body'][0]['number'],
                'doc_date': doc['body'][0]['docDate'],
                'doc_end_date': doc['body'][0]['endDate'],
                'doc_is_real': doc['body'][0]['is_real'],
                'doc_hwo_out': doc['body'][0]['hwo_out'],
                'True': True
             }
            except IndexError as err:
                print(err)
                return render(request, 'app/paper/fail_search.html', {'True': True})

            return render(request, 'app/paper/document.html', context=context)
    else:
        form = SearchForm()

    return render(request, 'app/paper/doc_search.html', {'form': form})

