from django import forms
from django.forms import ModelForm

from .models import TutorSesh


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


class TutorSeshForm(ModelForm):
    class Meta:
        model = TutorSesh
        fields = ['date','time']
        widgets= {
            'date': DateInput(),
            'time': TimeInput()
        }


class ClassSearchForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=50, required=False)
    catalog_nbr = forms.CharField(label='Class Number', max_length=50, required=False)
    descr = forms.CharField(label='Class Name', max_length=100, required=False)

class UpdateTheTutorProfileForm(forms.Form):
    username = forms.CharField(label="Username",widget=forms.Textarea)
    monday = forms.BooleanField(label= "Monday", required=False)
    tuesday = forms.BooleanField(label ="Tuesday",required=False)
    wednesday = forms.BooleanField(label = "Wednesday", required=False)
    thursday = forms.BooleanField(label="Thursday", required=False)
    friday = forms.BooleanField(label="Friday", required=False)
    saturday = forms.BooleanField(label="Saturday", required=False)
    sunday = forms.BooleanField(label="Sunday", required=False)
    phone_number = forms.CharField(label="Phone Number",max_length=12,required=False,)
    avail_start = forms.TimeField(label="Availability Start", widget=TimeInput)
    avail_end = forms.TimeField(label="Availibility End", widget=TimeInput)
    hourly_rate = forms.FloatField(label="Hourly Rate ($USD)",required=False)


class UpdateTheStudentProfileForm(forms.Form):
    username = forms.CharField(label="Username",widget=forms.Textarea)
    phone_number = forms.CharField(label="Phone Number",max_length=12,required=False,)
