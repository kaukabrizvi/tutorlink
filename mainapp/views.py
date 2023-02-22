from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.
def index(request):
    return HttpResponse("This will be the home page for the TutorLink app TEST.")


class studentLoginView(generic.ListView):
    template_name = 'studentLogin.html']
    context_object_name = 'student_login'