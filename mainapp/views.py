from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
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
        return redirect('tutor')
    
    if "studentbtn" in request.POST:
        Profile.objects.filter(user=request.user).update(is_student=True)
        return redirect('student')
    
def changeRole(request):
    Profile.objects.filter(user=request.user).update(is_tutor=False)
    Profile.objects.filter(user=request.user).update(is_student=False)
    return redirect('index')

def getAllTutors(request):
    tutors = Profile.objects.filter(is_tutor = False)
    context = {
        "Tutors" : tutors
    }
    return render(request,"tutorList.html",context)

#Got this from learndjango.com/tutorials/django-search-tutorial
class SearchResultsView(ListView):
    model = Profile
    template_name = "tutorList.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        found_tutors = Profile.objects.filter(is_tutor=True)
        return found_tutors