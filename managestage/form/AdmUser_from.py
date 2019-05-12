from django import forms

class add_user_From(forms.Form):
    email = forms.CharField(label='邮箱')
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码')

    pass


class set_prohibit_From(forms.Form):
    email = forms.CharField(label='邮箱')
    username = forms.CharField(label='用户名')
    prohi_datetime = forms.CharField(label='封禁时间段')
    prohi_text = forms.CharField(label='封禁原因')
