from django import forms

from app.models import Navaid, NavaidImages, NavaidMiddle, NavaidMiddleWareApp

class pageFrom(forms.ModelForm):

    class Meta:
        model = Navaid
        fields = ['site_navaid_tags'] # '__all__'


class pageImageForm(forms.Form):

    class Meta:
        model = NavaidImages
        fields = ['images']
    pass


class pageNavPlateForm(forms.Form):

    class Meta:
        model = NavaidMiddle
        fields = ['navaid_name', 'navaid_urls', 'navaid_images']


class pageNavWareAppeForm(forms.Form):

    class Meta:
        model = NavaidMiddleWareApp
        fields = ['navaid_name', 'navaid_number']



