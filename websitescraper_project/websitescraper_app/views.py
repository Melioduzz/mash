import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from bs4 import BeautifulSoup

from .models import Links


# Create your views here.
def index(request):
    if request.method == 'POST':
        link_new = request.POST.get('page', '')
        urls = requests.get(link_new)
        beautifulsoup = BeautifulSoup(urls.text, 'html.parser')
        for link in beautifulsoup.find_all('a'):
            li_address = link.get('href')
            li_name = link.string
            Links.objects.create(address=li_address, Stringname=li_name)
        return HttpResponseRedirect('/')
    data_values = Links.objects.all()

    return render(request, "index.html", {'data_values': data_values})
