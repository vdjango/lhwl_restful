from django import forms

class Form1(forms.Form):
    name = forms.CharField(max_length=50, label='说明摘要')
    url = forms.CharField(max_length=100, label='超链接地址')
    image = forms.ImageField()


class Form2(forms.Form):
    name = forms.CharField(max_length=50, label='说明摘要')
    #url = forms.CharField(max_length=100, label='超链接地址')
    #defaule = forms.BooleanField(label='默认状态[表示首页]')
    #image = forms.ImageField()