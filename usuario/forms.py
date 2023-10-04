from django import forms
from django.contrib.admin import widgets
import django.forms.widgets 
import datetime


class CargarArchivoForm(forms.Form):
    archivo = forms.FileField()

class ExcelForm(forms.Form):
    year = (datetime.date.today()).strftime("%Y")
    YEARS = []
    for i in range(10):
        f = int(year) - i
        YEARS.append(str(f))

    fechaDescarga = forms.DateField(
    widget=forms.SelectDateWidget(
        years=YEARS
    ))
    # fechaDescarga2 = forms.DateField(widget=forms.SelectDateWidget)