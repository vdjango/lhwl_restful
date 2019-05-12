
from django import forms
from app import models


class WareParProfixForm(forms.ModelForm):

    class Meta:
        model = models.WareParProfix
        fields = '__all__'




# self.fields['filter_name'].widget.choices = 0
