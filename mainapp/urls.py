"""tutorlink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views
from .views import SearchResultsView
app_name = "mainapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('student',TemplateView.as_view(template_name="mainapp/studentLogin.html"), name='student'),
    path('tutor', TemplateView.as_view(template_name="mainapp/tutorLogin.html"), name='tutor'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('admin', admin.site.urls),
    path('user/assign',views.assignUserType, name='apply-type'),
    path('changerole/', views.changeRole, name='change-role'),
    path('departments/', views.department_list, name='department_list'),
    path('courses/<str:mnemonic>/', views.course_list, name='course_list'),
    path('classes/<str:class_title>/', views.select_class, name='select_class'),
    path('student/allTutors', views.getAllTutors, name="tutorList"),
    path('student/allTutors/results', SearchResultsView.as_view(), name='tutorSearch'),
    path('classadded', views.add_class_to_profile, name="add-class"),
    path('myCourses', views.viewMyCourses, name="myCourses"),
    path('myProfile', views.myProfile,name="profile"),
    path('student/allTutors/results/addTutor', views.add_tutor_to_profile, name="add-tutor"),
    path('student/myTutors',views.myTutorList, name="studentTutorsList"),
    path('tutor/myStudents', views.myStudentList, name="myStudents"),
    path('tutor/myStudents/acceptStudent', views.accept_student_to_profile, name="accept-student"),
    path('load_from_api/', views.load_from_api, name='load_from_api'),
]
