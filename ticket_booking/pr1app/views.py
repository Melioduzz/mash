from django.http import HttpResponse
from django.shortcuts import render
from . models import Place
from . models import Packages

# Create your views here.
def demo(request):
    obj = Place.objects.all()
    pack = Packages.objects.all()
    return render(request,"index.html",{'result':obj,'packages':pack})
