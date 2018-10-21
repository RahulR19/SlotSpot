from django import forms
from django.forms import ModelForm
from personal.models import Reserve
from personal.models import Cancel
from personal.models import Item
from personal.models import Dates
from django.core.validators import MinValueValidator, MaxValueValidator

class ReserveForm(ModelForm):
    class Meta:
        model = Reserve
        exclude = ['Instrument','Time','Date']

        def clean(self):
            super().clean()
            Rollno      = self.cleaned_data.get['Rollno']
            First       = self.cleaned_data.get['First']
            Last        = self.cleaned_data.get['Last']
            Email       = self.cleaned_data.get['Email']
            Phone       = self.cleaned_data.get['Phone']
            Pin         = self.cleaned_data.get['Pin']

class DateForm(ModelForm):
    class Meta:
        model = Dates
        fields = '__all__'

        def clean(self):
            super().clean()
            Date        = self.cleaned_data.get['Date']

class CancelForm(ModelForm):
    class Meta:
        model = Cancel
        fields = '__all__'

        def clean(self):
            super().clean()
            Rollno = self.cleaned_data.get['Rollno']
            Pin   = self.cleaned_data.get['Pin']

form = ReserveForm()
form2 = CancelForm()
form3 = DateForm()
