from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.urls import reverse
from django.shortcuts import redirect
from .models import Profile, Course, TutorSesh
from .forms import TutorSeshForm
from calendar import HTMLCalendar
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
    courses = {}

    for c in response:
        name = c['subject'] + " " + c['catalog_nbr']
        courses[name] = True
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
    form_class = TutorSeshForm
    def get(self,request):
        form = self.form_class()
        query = self.request.GET.get("q")
        found_tutors = Profile.objects.filter(is_tutor=True).filter(user__username__contains=query)
        return render(request,self.template_name,{'form' : form, 'tutors' : found_tutors})

def viewMyCourses(request):
    classes = Profile.objects.filter(user = request.user).values("classes")
    print(classes[0]["classes"])
    context = {
        "courses" : classes[0]["classes"]
    }
    return render(request,"mainapp/myClasses.html", context)

def myProfile(request):
    theUser = Profile.objects.get(user=request.user)
    if theUser.is_student:
       return redirect('student')
    elif theUser.is_tutor:
        return redirect('tutor')
    else:
        return Http404

def add_tutor_to_profile(request): #need to figure out how we're going to connect them
        theUser = Profile.objects.get(user=request.user)
        if "tutor" in request.POST:
            theTutor = Profile.objects.get(user=request.POST["tutor"])
            theSesh = TutorSesh.objects.create(
                tutor=theTutor.user,
                student = theUser.user,
                date = request.POST["date"],
                time = request.POST["time"],)
            theSesh.save()
            theUser.connected_list.add(theTutor.user)
            theUser.schedule_list.add(theSesh)
            theUser.save()
            theTutor.connected_list.add(theUser.user)
            theTutor.schedule_list.add(theSesh) #need to use .all() to retrieve associated objects
            theTutor.save()
            return redirect("student")
        else:
            return myProfile(request)
def accept_student_to_profile(request): 
        theSesh = TutorSesh.objects.get(id=request.POST["sesh"])
        theUser = Profile.objects.get(user=theSesh.tutor)
        theStudent = Profile.objects.get(user=theSesh.student)
        #theSesh = theStudent.schedule_list.get(tutor=theUser.user, student = theStudent.user, )
        if request.method == "POST":
            theUser.accepted_list.add(theStudent.user)
            theUser.connected_list.remove(theStudent.user)
            theUser.save()
            theStudent.accepted_list.add(theUser.user)
            theStudent.connected_list.remove(theUser.user)  
            theUser.schedule_list.add(theSesh)
            theStudent.save()
            return redirect("tutor")

def myTutorList(request):
    user = Profile.objects.get(user=request.user)
    context = {
        "requests" : user.connected_list.all(),
        "tutors" : user.accepted_list.all(),
        "seshs" : user.schedule_list.all()
    }
    return render(request, "mainapp/myTutors.html", context)

def myStudentList(request):
    user = Profile.objects.get(user=request.user)
    context = {
        "students" : user.connected_list.all(),
        "accepted" : user.accepted_list.all(),
        "seshs" : user.schedule_list.all(),
    }
    return render(request, "mainapp/myStudents.html", context)


# def mySchedule(request):
#     context= {

#     }
#     return render(request,"mainapp/scedule.html",context)

