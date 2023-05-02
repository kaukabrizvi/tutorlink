from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.urls import reverse
from django.shortcuts import redirect
from django.db import transaction
from .models import Profile, Class, TutorSesh
from .forms import TutorSeshForm, UpdateTheTutorProfileForm, UpdateTheStudentProfileForm
from calendar import HTMLCalendar
from django.db.models import Q
from .forms import ClassSearchForm
from django.contrib.auth.decorators import login_required
from .models import Tutor, Review
import datetime
from django.contrib import messages
from django.utils.timezone import localtime, now
import requests
import operator

# Create your views here.
"""
Refrences:
-----------------
For the SearchResultsView
Title: Djanog Search Tutorial
Author: Will Vincent
URL : learndjango.com/tutorials/django-search-tutorial
------------------------------

"""
"""
*  For Reviews
*  Title: Reviews Function
*  Author: W3 Schools
*  Code version: HTML
*  URL: https://www.w3schools.com/howto/howto_css_user_rating.asp
*  Software License: <license software is released under>

"""



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
    if request.method == 'POST':
        print(request.POST)
        class_val = request.POST["add_class"]  # Updated line
        subject, catalog_nbr = class_val.split(" ")
        class_obj = Class.objects.get(subject=subject, catalog_nbr=catalog_nbr)
        profile = request.user.profile
        profile.classes.add(class_obj)
        # Check if the user is a tutor
        if request.user.profile.is_tutor:
            
            
            # Add the user to the class's list of tutors
            class_obj.tutors.add(request.user)
            
        return redirect('index')
    
    return render(request, 'mainApp/classinfo.html', {'course': course})

def remove_class_from_profile(request):
    if request.method == 'POST':
        print(request.POST)
        class_val = request.POST["remove_class"]  # Updated line
        subject, catalog_nbr = class_val.split(" ")
        class_obj = Class.objects.get(subject=subject, catalog_nbr=catalog_nbr)
        profile = request.user.profile
        profile.classes.remove(class_obj)
        if request.user.profile.is_tutor:
            class_obj.tutors.remove(request.user)

        return redirect('index')
    return render(request, 'mainapp/classinfo.html', {'course': course})

def expand_class(request, course_id):
    course = get_object_or_404(Class, id=course_id)
    user = request.user
    can_add_class = not user.profile.classes.filter(id=course_id).exists()
    tutors = list(course.tutors.all())
    return render(request, "mainapp/classInfo.html", {
        'subject': course.subject,
        'catalog_nbr': course.catalog_nbr,
        'descr': course.descr,
        'can_add_class': can_add_class,
        'tutors': tutors
    })
def getAllTutors(request):
    theUser = Profile.objects.get(user=request.user)
    tutors = Profile.objects.filter(is_tutor = True).filter(classes__in=theUser.classes.all())
    context = {
        "Tutors" : tutors
    }
    return render(request,"mainapp/tutorList.html",context)

class SearchResultsView(ListView):
    model = Profile
    template_name = "mainapp/tutorList.html"
    form_class = TutorSeshForm
    def get(self,request):
        form = self.form_class()
        query = self.request.GET.get("q")
        print(request.user)
        theUser = Profile.objects.get(user=request.user)
        if query != None:
            found_tutors = Profile.objects.filter(is_tutor=True).filter(user__username__contains=query).filter(classes__in=theUser.classes.all())
        else:
           found_tutors = None
        return render(request,self.template_name,{'form' : form, 'tutors' : found_tutors.order_by('-rating')})

def viewMyCourses(request):
    profile = request.user.profile
    classes = profile.classes.all()
    context = {
        "courses" : classes
    }
    return render(request, "mainapp/myClasses.html", context)

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
            theDate = datetime.datetime.strptime(request.POST["date"],"%Y-%m-%d")
            theTime = datetime.datetime.strptime(request.POST["time"],"%H:%M").time()
            #dates = { #use this to do the comparison dynamically for day of the week
            #    0 : theTutor.monday,
            #    1 : theTutor.tuesday,
            #    2 : theTutor.wednesday,
            #    3 : theTutor.thursday,
            #    4 : theTutor.friday,
            #    5 : theTutor.saturday,
            #    6 : theTutor.sunday,
            #}
            day_start = {
                0 : theTutor.mon_avail_start,
                1 : theTutor.tue_avail_start,
                2 : theTutor.wed_avail_start,
                3 : theTutor.thu_avail_start,
                4 : theTutor.fri_avail_start,
                5 : theTutor.sat_avail_start,
                6 : theTutor.sun_avail_start,
            }
            day_end = {
                0 : theTutor.mon_avail_end,
                1 : theTutor.tue_avail_end,
                2 : theTutor.wed_avail_end,
                3 : theTutor.thu_avail_end,
                4 : theTutor.fri_avail_end,
                5 : theTutor.sat_avail_end,
                6 : theTutor.sun_avail_end,
            }
            
            if theDate >= datetime.datetime.now() and (day_start[theDate.weekday()] < theTime < day_end[theDate.weekday()]) and theTime > localtime:
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
                return redirect("index")
            else:  
                messages.warning(request, "Cannot request tutor when they aren't available.")
                return HttpResponseRedirect(reverse("tutorSearch"))
                
def accept_student_to_profile(request): 
        print(request.POST)
        for sesh in request.POST.getlist('sesh'):
            print(sesh)
            theSesh = TutorSesh.objects.get(id=int(sesh))
            theUser = Profile.objects.get(user=theSesh.tutor)
            theStudent = Profile.objects.get(user=theSesh.student)
            if request.method == "POST" and "accept" in request.POST:
                theSesh.accepted = True
                theSesh.save()
                theUser.accepted_list.add(theStudent.user)
                seshlist= []
                for sesh in theUser.schedule_list.all():
                    if sesh.student == theStudent.user and not sesh.accepted:
                        seshlist.append(sesh)
                if len(seshlist) == 0:
                    theUser.connected_list.remove(theStudent.user)
                    theStudent.connected_list.remove(theUser.user) 
                
                theUser.save()
                theStudent.accepted_list.add(theUser.user) 
                theUser.schedule_list.add(theSesh)
                theStudent.save()
            else:
                seshlist= []
                for sesh in theUser.schedule_list.all():
                    if sesh.student == theStudent.user and not sesh.accepted:
                        seshlist.append(sesh)
                if len(seshlist) == 0:
                    theUser.connected_list.remove(theStudent.user)
                    theStudent.connected_list.remove(theUser.user)
                
                theUser.save()
                theStudent.save()
                theSesh.delete()
        return redirect("index")

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

def load_from_api(request):
    term = '1238'
    # Get the list of department mnemonics
    options_url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term={term}'
    response = requests.get(options_url).json()
    mnemonics = []
    # Render the template with the list of mnemonics
    for s in response['subjects']:
        mnemonics.append(s['subject'])
    classes = {}
    for c in mnemonics:
        s = c.upper()
        url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}'
        response = requests.get(url + '&subject=' + s + '&page=1').json()
        for x in response:
            name = x['subject'] + " " + x['catalog_nbr'] + " " + x['descr']
            classes[name] = True
    url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term={term}'
    courses = []
    for key in classes:
        n = key.split()
        descr = " ".join(n[2:])
        courses.append(Class(subject=n[0], catalog_nbr=n[1], descr=descr))

    with transaction.atomic():
        Class.objects.bulk_create(courses)

    return render(request, 'mainapp/load_from_api.html')


# def mySchedule(request):
#     context= {

#     }
#     return render(request,"mainapp/scedule.html",context)


def search_classes(request):
    if request.method == 'GET':
        form = ClassSearchForm(request.GET)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            catalog_nbr = form.cleaned_data.get('catalog_nbr')
            descr = form.cleaned_data.get('descr')

            query = Q()

            if subject:
                query &= Q(subject__icontains=subject)

            if catalog_nbr:
                query &= Q(catalog_nbr__icontains=catalog_nbr)

            if descr:
                query &= Q(descr__icontains=descr)

            classes = Class.objects.filter(query)

            if 'descr' in request.GET and request.GET['descr'] and not 'subject' in request.GET and not 'catalog_nbr' in request.GET:
                url = f"/search_classes/?subject=&catalog_nbr=&descr={request.GET['descr']}"
                return redirect(url)

            context = {
                'classes': classes,
                'form': form
            }

            return render(request, 'mainapp/search_results.html', context)

    else:
        form = ClassSearchForm()

    context = {'form': form}
    return render(request, 'mainapp/search_classes.html', context)

class TutorProfileEditView(ListView):
    model = Profile
    template_name = "mainapp/edit_tutor_profile.html"
    form_class = UpdateTheTutorProfileForm 
    """
    ADD SEPERATE FORM FOR TUTOR AND STUDENT SINCE THEY'RE GONNA HAVE DIFFERENT FIELDS
    """
    def get(self,request):
        form = self.form_class()
        theUser = Profile.objects.get(user=request.user)
        form.fields['username'].initial = theUser.user.username
        form.fields['monday'].initial = theUser.monday
        form.fields['tuesday'].initial = theUser.tuesday
        form.fields['wednesday'].initial = theUser.wednesday
        form.fields['thursday'].initial = theUser.thursday
        form.fields['friday'].initial = theUser.friday
        form.fields['saturday'].initial = theUser.saturday
        form.fields['sunday'].initial = theUser.sunday
        form.fields['mon_avail_start'].initial = theUser.mon_avail_start
        form.fields['mon_avail_end'].initial = theUser.mon_avail_end
        form.fields['tue_avail_start'].initial = theUser.tue_avail_start
        form.fields['tue_avail_end'].initial = theUser.tue_avail_end
        form.fields['wed_avail_start'].initial = theUser.wed_avail_start
        form.fields['wed_avail_end'].initial = theUser.wed_avail_end
        form.fields['thu_avail_start'].initial = theUser.thu_avail_start
        form.fields['thu_avail_end'].initial = theUser.thu_avail_end
        form.fields['fri_avail_start'].initial = theUser.fri_avail_start
        form.fields['fri_avail_end'].initial = theUser.fri_avail_end
        form.fields['sat_avail_start'].initial = theUser.sat_avail_start
        form.fields['sat_avail_end'].initial = theUser.sat_avail_end
        form.fields['sun_avail_start'].initial = theUser.sun_avail_start
        form.fields['sun_avail_end'].initial = theUser.sun_avail_end
        form.fields['phone_number'].initial = theUser.phone_number
        form.fields['hourly_rate'].initial = theUser.hourly_rate
        form.fields['bio'].initial = theUser.bio
        return render(request,self.template_name,{'form' : form})



#Googled what were some functions i could use to get attributes, didn't exactly copy any specific code
def TutorProfileEdit(request):
    form = UpdateTheTutorProfileForm(request.POST)
    if form.is_valid():
        theUser = Profile.objects.get(user=request.user)
        days_list = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        for key in request.POST:
            if key == "username":
                print("IN HERE")
                theUser.user.username = request.POST[key]
                print(theUser.user.username)
                theUser.user.save()
            elif hasattr(theUser,key):
                if request.POST[key] == "on": #this is for the checkboxes
                    setattr(theUser,key,True)
                    days_list.remove(key)
                else:
                    setattr(theUser,key,request.POST[key])
        for day in days_list:
            setattr(theUser,day,False)
        theUser.save()
        return redirect('index')
    else:
        return render(request, "mainapp/edit_tutor_profile.html" ,{'form' : form})
    

class StudentProfileEditView(ListView):
    model = Profile
    template_name = "mainapp/edit_student_profile.html"
    form_class = UpdateTheStudentProfileForm 
    """
    ADD SEPERATE FORM FOR TUTOR AND STUDENT SINCE THEY'RE GONNA HAVE DIFFERENT FIELDS
    """
    def get(self,request):
        form = self.form_class()
        theUser = Profile.objects.get(user=request.user)
        form.fields['username'].initial = theUser.user.username
        form.fields['phone_number'].initial = theUser.phone_number
        return render(request,self.template_name,{'form' : form})

def StudentProfileEdit(request):
    theUser = Profile.objects.get(user=request.user)
    for key in request.POST:
        if key == "username":
            theUser.user.username = request.POST[key]
            print(theUser.user.username)
            theUser.user.save()
        else:
            setattr(theUser,key,request.POST[key])
    theUser.save()
    return redirect('index')

@login_required
def submit_review(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        review = Review(tutor=tutor, student=request.user, rating=rating, comment=comment)
        review.save()
        tutor.update_rating()
        return redirect('tutor_detail', tutor_id=tutor.id)
    return render(request, 'submit_review.html', {'tutor': tutor})


def getTutorProfile(request,tutor_id):
    tutor = Profile.objects.get(id=tutor_id)
    theUser = Profile.objects.get(user=request.user)
    return render(request, 'mainapp/tutorProfile.html', {'tutor' : tutor, 'form' : TutorSeshForm, 'user' : theUser})


def add_tutor_to_profile_from_profile(request):
        theUser = Profile.objects.get(user=request.user)
        if "tutor" in request.POST:
            theTutor = Profile.objects.get(user=request.POST["tutor"])
            theDate = datetime.datetime.strptime(request.POST["date"],"%Y-%m-%d")
            theTime = datetime.datetime.strptime(request.POST["time"],"%H:%M").time()
            dates = { #use this to do the comparison dynamically for day of the week
                0 : theTutor.monday,
                1 : theTutor.tuesday,
                2 : theTutor.wednesday,
                3 : theTutor.thursday,
                4 : theTutor.friday,
                5 : theTutor.saturday,
                6 : theTutor.sunday,
            }
            day_start = {
                0 : theTutor.mon_avail_start,
                1 : theTutor.tue_avail_start,
                2 : theTutor.wed_avail_start,
                3 : theTutor.thu_avail_start,
                4 : theTutor.fri_avail_start,
                5 : theTutor.sat_avail_start,
                6 : theTutor.sun_avail_start,
            }
            day_end = {
                0 : theTutor.mon_avail_end,
                1 : theTutor.tue_avail_end,
                2 : theTutor.wed_avail_end,
                3 : theTutor.thu_avail_end,
                4 : theTutor.fri_avail_end,
                5 : theTutor.sat_avail_end,
                6 : theTutor.sun_avail_end,
            }
            if dates[theDate.weekday()] and ((theDate.date() == datetime.datetime.now().date() and theTime > localtime().time()) or (theDate.date() > datetime.datetime.now().date())) and (day_start[theDate.weekday()] < theTime < day_end[theDate.weekday()]):
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
                return redirect("index")
            else:
                messages.warning(request, "Cannot request tutor when they aren't available.")
                return HttpResponseRedirect(reverse('tutor-profile',kwargs={'tutor_id' : request.POST["tutor"]}))


def review_page(request, sesh_id):
    user = Profile.objects.get(user=request.user)
    context = {
        "sesh" : TutorSesh.objects.get(id=sesh_id),
        "tutor": TutorSesh.objects.get(id=sesh_id).tutor,
        "is_upcoming": TutorSesh.objects.get(id=sesh_id).is_upcoming()
    }
    return render(request, "mainapp/review.html", context)


def update_rating(request):
    theTutor = Profile.objects.get(user=request.POST["tutor"])
    theUser = Profile.objects.get(user=request.user)
    theSesh = TutorSesh.objects.get(id=request.POST["sesh"])

    the_rating = int(request.POST["rating"])

    theTutor.review_count += 1
    theTutor.rating = (theTutor.rating*(theTutor.review_count-1) + the_rating) / theTutor.review_count

    theSesh.has_rated = True
    theSesh.save()
    theUser.schedule_list.remove(theSesh)
    theTutor.schedule_list.remove(theSesh)
    theTutor.save()
    theUser.save()

    return redirect('index')
