from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
# Create your views here.


def index(request):
    return render(request,"mainapp/landing_page.html")

#Assigns user type
def assignUserType(request):
    if "tutorbtn" in request.POST:
        theUser = request.user
        theUser.is_tutor = True
        theUser.save()
        print(theUser.is_tutor)
        return redirect('index')
    
    if "studentbtn" in request.POST:
        theUser = request.user
        theUser.is_student = True
        theUser.save()
        return redirect('index')