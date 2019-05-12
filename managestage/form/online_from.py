from django import forms

class Form_one(forms.Form):
    name = forms.CharField(max_length=255, label='配置')
    money = forms.CharField(max_length=12, label='套餐价')

class Form_two(forms.Form):
    name = forms.CharField(max_length=20, label='时间')

