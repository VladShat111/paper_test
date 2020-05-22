# Create your views here.
from functools import wraps
from django.shortcuts import render
import requests
from datetime import datetime
from .forms import TokenRetrieveForm
from django.contrib import messages
from django.shortcuts import reverse, redirect
from .models import Person
# Create your views here.


def token_exp(something):
    @wraps(something)
    def wrap(*args, **kwargs):
        req = args[1]
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

            token = requests.post('http://mainapi.hsc.gov.ua/auth-server/oauth/token', data=dat,
                                  auth=(client_id, client_secret)).json()

            request.session['token'] = 'Bearer ' + token['access_token']
            request.session['expires_in'] = token['expires_in'] + datetime.now().timestamp()

            messages.success(request, 'Success! Now you have a permission to get your paper. Use links under to do it.')
            person, created = Person.objects.get_or_create(username=dat['username'], clntId=client_id)

            return redirect(reverse('get_paper', kwargs={'paper_pk': person.paper_id}))

    else:
        form = TokenRetrieveForm()

    return render(request, 'app/paper/token_retrieve.html', {'form': form})



def get_paper(request, paper_pk):

    header = {'Authorization': request.session['token']}

    paper = requests.get(f'http://mainapi.hsc.gov.ua/tst-sprlics-service/sprlics/{paper_pk}', headers=header).json()

    request.session['clntId'] = paper[0]['clntId']
    request.session['carId'] = paper[0]['carId']
    request.session['licencePlate'] = paper[0]['licencePlate']
    request.session['vin'] = paper[0]['vin']
    request.session['seria'] = paper[0]['seria']
    request.session['number'] = paper[0]['number']

    context = {'paper': paper[0], 'clntId_con': paper[0]['clntId'],
               'carId_con': paper[0]['carId'], 'vin_con': paper[0]['vin']}

    return render(request, 'app/paper/paper.html', context)


def get_person(request, cltId):

    header = {'Authorization': request.session['token']}
    person = requests.get(f"http://mainapi.hsc.gov.ua/tst-sprlics-service/sprlics/person/{cltId}",
                            headers=header).json()

    context = {'person': person[0]}

    return render(request, 'app/paper/person.html', context)


def get_car(request, carId):

    header = {'Authorization': request.session['token']}

    car = requests.get(f"http://mainapi.hsc.gov.ua/tst-sprlics-service/sprlics/car/{carId}",
                       headers=header).json()
    return render(request, 'app/paper/car.html', {'car': car})


def get_car_licence(request):

    header = {'Authorization': request.session['token']}
    param = {'licencePlate': request.session['licencePlate']}
    cars = requests.get(f"http://mainapi.hsc.gov.ua/tst-sprlics-service/sprlics/car",
                       headers=header, params=param).json()

    return render(request, 'app/paper/car_licence.html', {'cars': cars})


def get_sprlics(request):

    header = {'Authorization': request.session['token']}
    param = {'seria': request.session['seria'], 'number': request.session['number']}
    sprlics = requests.get('http://mainapi.hsc.gov.ua/tst-sprlics-service/sprlics',
                           headers=header, params=param).json()

    return render(request, 'app/paper/sprlics.html', {'sprlics': sprlics[0]})


def get_vin(request, vin_number):

    header = {'Authorization': request.session['token']}
    get_vin = requests.get(f"http://mainapi.hsc.gov.ua/tst-sprlics-service/sprlics/vin/{vin_number}",
                           headers=header).json()

    return render(request, 'app/paper/vin.html', {'vin': get_vin})

