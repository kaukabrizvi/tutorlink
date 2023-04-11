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
