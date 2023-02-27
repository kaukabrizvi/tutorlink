from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
from .models import Profile
# Create your views here.


def index(request):
    user = Profile.objects.all()
    context = {
        "Profiles" : user
    }
    return render(request,"mainapp/landing_page.html",context)

#Assigns user type
def assignUserType(request):
    if "tutorbtn" in request.POST:
        Profile.objects.filter(user=request.user).update(is_tutor=True)
        return redirect('index')
    
    if "studentbtn" in request.POST:
        Profile.objects.filter(user=request.user).update(is_student=True)
        return redirect('index')
    
def changeRole(request):
    Profile.objects.filter(user=request.user).update(is_tutor=False)
    Profile.objects.filter(user=request.user).update(is_student=False)
    return redirect('index')
