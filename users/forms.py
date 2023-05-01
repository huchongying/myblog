from django import forms
from django.forms import ModelForm

from users.models import User, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100, widget=forms.TextInput)
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class RegisterForm(forms.ModelForm):
    """注册表单"""
    email = forms.EmailField(label='邮箱', min_length=3, widget=forms.EmailInput)
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput)
    password1 = forms.CharField(label='再次密码', min_length=6, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

    class Meta:
        model = User  # 这里的model是User，不是UserProfile
        fields = ('email', 'password')

    def clean_username(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("邮箱已经存在！")
        return email

    # 这里的clean_password1是自定义的，不是系统自带的，所以要在下面的cleaned_data中添加，否则会报错，
    # 找不到password1，因为系统自带的cleaned_data中没有password1
    def clean_password1(self):
        data = self.cleaned_data
        password = data['password']
        password1 = data['password1']
        if password != password1:
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return password


# 忘记密码
class ForgetPwdForm(forms.Form):
    """ 填写邮箱地址表单 """
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))


# 重置密码
class ModifyPwdForm(forms.Form):
    """ 重置密码表单 """
    password = forms.CharField(label='输入新密码', min_length=6,
                               widget=forms.PasswordInput(attrs={'placeholder': '请输入新密码'}))

    def __init__(self, *args, **kwargs):
        super(ModifyPwdForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('nike_name', 'desc', 'gexing', 'birthday', 'gender', 'adress', 'image')

        def __init__(self, *args, **kwargs):
            super(UserProfileForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'input'})