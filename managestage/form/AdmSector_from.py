from django import forms

from app.models import RateClassgUid
from home import models


class Form_Discount(forms.ModelForm):
    '''
    商品提交表单验证
    '''
    class Meta:
        model = models.Discount
        fields = ['a1', 'a2', 'a3', 'a4']


class RateClassgUidForm(forms.ModelForm):
    '''
    商品提交表单验证
    '''
    class Meta:
        model = RateClassgUid
        fields = ['uid', 'a1', 'a2', 'a3', 'a4']

