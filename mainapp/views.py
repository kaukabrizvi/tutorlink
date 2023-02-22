from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
# Create your views here.


def index(request):
    return render(request,"mainapp/index.html")

