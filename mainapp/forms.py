from django import forms
from django.forms import ModelForm
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.layout import Layout
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
    subject = forms.CharField(label='Mnemonic', max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. MATH, CS'}))
    catalog_nbr = forms.CharField(label='Class Number', max_length=50, required=False,  widget=forms.TextInput(attrs={'placeholder': 'e.g. 1010'}))
    descr = forms.CharField(label='Class Name', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. Advanced Software'}))

class UpdateTheTutorProfileForm(forms.Form):
    username = forms.CharField(label="Username",widget=forms.Textarea(attrs={'cols': 20, 'rows': 1}))
    monday = forms.BooleanField(label= "Monday", required=False)
    mon_avail_start = forms.TimeField(label="Monday Availability Start", widget=TimeInput)
    mon_avail_end = forms.TimeField(label="Monday Availibility End", widget=TimeInput)

    tuesday = forms.BooleanField(label ="Tuesday",required=False)
    tue_avail_start = forms.TimeField(label="Tuesday Availability Start", widget=TimeInput)
    tue_avail_end = forms.TimeField(label="Tuesday Availibility End", widget=TimeInput)

    wednesday = forms.BooleanField(label = "Wednesday", required=False)
    wed_avail_start = forms.TimeField(label="Wednesday Availability Start", widget=TimeInput)
    wed_avail_end = forms.TimeField(label="Wednesday Availibility End", widget=TimeInput)

    thursday = forms.BooleanField(label="Thursday", required=False)
    thu_avail_start = forms.TimeField(label="Thursday Availability Start", widget=TimeInput)
    thu_avail_end = forms.TimeField(label="Thursday Availibility End", widget=TimeInput)

    friday = forms.BooleanField(label="Friday", required=False)
    fri_avail_start = forms.TimeField(label="Friday Availability Start", widget=TimeInput)
    fri_avail_end = forms.TimeField(label="Friday Availibility End", widget=TimeInput)

    saturday = forms.BooleanField(label="Saturday", required=False)
    sat_avail_start = forms.TimeField(label="Saturday Availability Start", widget=TimeInput)
    sat_avail_end = forms.TimeField(label="Saturday Availibility End", widget=TimeInput)
    
    sunday = forms.BooleanField(label="Sunday", required=False)
    sun_avail_start = forms.TimeField(label="Sunday Availability Start", widget=TimeInput)
    sun_avail_end = forms.TimeField(label="Sunday Availibility End", widget=TimeInput)  
    
    phone_number = forms.CharField(label="Phone Number",max_length=12,required=False,)
    #avail_start = forms.TimeField(label="Availability Start", widget=TimeInput)
    #avail_end = forms.TimeField(label="Availibility End", widget=TimeInput)
    hourly_rate = forms.FloatField(label="Hourly Rate ($USD)",required=False)
    bio = forms.CharField(label="Bio", widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False)


class UpdateTheStudentProfileForm(forms.Form):
    username = forms.CharField(label="Username",widget=forms.Textarea(attrs={'cols': 20, 'rows': 1}))
    phone_number = forms.CharField(label="Phone Number",max_length=12,required=False,)