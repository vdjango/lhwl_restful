from django import forms

from home import models


class Form_Address(forms.ModelForm):
    '''
    商品提交表单验证
    '''
    class Meta:
        model = models.Address
        fields = ['consigneeName', 'province', 'city', 'consigneeAddress', 'consigneeMobile']
