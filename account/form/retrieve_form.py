from django import forms

class Form(forms.Form):
    email = forms.CharField(max_length=100, label='邮箱或用户名')

class new_passwd(forms.Form):
    email = forms.CharField(max_length=100, label='邮箱或用户名')
    auto = forms.CharField(max_length=300, label='验证码')
    password = forms.CharField(max_length=100, label='密码')