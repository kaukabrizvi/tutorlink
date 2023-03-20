from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import redirect
from .models import Profile, Course
import requests
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


def department_list(request):
    # Set the term to the appropriate value (1 + 2 digit year + 2 for Spring, 8 for Fall)
    term = '1238'
    # Get the list of department mnemonics
    options_url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term={term}'
    response = requests.get(options_url).json()
    mnemonics = []
    # Render the template with the list of mnemonics
    for s in response['subjects']:
        mnemonics.append(s['subject'])
    query = request.GET.get('query')
    if query:
        matching_mnemonics = [m for m in mnemonics if query.upper() in m]
        if len(matching_mnemonics) == 0:
            raise Http404("No matching departments found.")
        elif len(matching_mnemonics) == 1:
            return redirect(reverse('course_list', kwargs={'mnemonic': matching_mnemonics[0]}))
        else:
            return render(request, 'mainapp/department_list.html', {'mnemonics': matching_mnemonics})
    return render(request, 'mainapp/department_list.html', {'mnemonics': mnemonics})

def course_list(request, mnemonic):
    # Set the term to the appropriate value (1 + 2 digit year + 2 for Spring, 8 for Fall)
    term = '1238'
    s = mnemonic.upper()
    # Get the list of courses for the specified department mnemonic
    url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}&subject={mnemonic}&page=1'
    response = requests.get(url + '&subject=' + s).json()
    courses = []

    for c in response:
        courses.append(c['subject'] + " " + c['catalog_nbr'])
    # Render the template with the list of courses
    return render(request, 'mainapp/course_list.html', {'courses': courses})
def select_class(request, class_title):
    term = '1238'
    s = class_title.upper().split()
    url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}'

    response = requests.get(url + '&subject=' + (s[0]) + '&catalog_nbr=' + s[1])
    classInfo= response.json()[0]
    return render(request, "mainapp/classInfo.html", {
        'subject': classInfo['subject'],
        'catalog_nbr': classInfo['catalog_nbr'],
        'descr': classInfo['descr'],
    })
def add_class_to_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.classes.append(request.POST["add_class"])
        profile.save()
        return redirect('department_list')
    
    return render(request, 'mainApp/classinfo.html', {'course': course})

def getAllTutors(request):
    tutors = Profile.objects.filter(is_tutor = False)
    context = {
        "Tutors" : tutors
    }
    return render(request,"mainapp/tutorList.html",context)

#Got this from learndjango.com/tutorials/django-search-tutorial
class SearchResultsView(ListView):
    model = Profile
    template_name = "mainapp/tutorList.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        found_tutors = Profile.objects.filter(is_tutor=True).filter(user__username__contains=query)
        return found_tutors

def viewMyCourses(request):
    classes = Profile.objects.filter(user = request.user).values("classes")
    print(classes[0]["classes"])
    context = {
        "courses" : classes[0]["classes"]
    }
    return render(request,"mainapp/myClasses.html", context)

