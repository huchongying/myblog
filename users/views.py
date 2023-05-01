from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required  # 登陆验证装饰器
from django.http import HttpResponse
from django.shortcuts import render, redirect
from sqlalchemy.sql.functions import user

from users.models import User, EmailVerifyRecord, UserProfile
from django.contrib.auth.hashers import make_password  # 加密,解密,加密后的密码不可逆
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
from django.contrib.auth.backends import ModelBackend  # 邮箱验证,用户名验证
from django.db.models import Q
from utils.email_send import send_register_email
from django.contrib.auth import logout  # 退出登录的包
from django.core.paginator import Paginator  # 分页

# Create your views here.
def user_login(request):
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # 登陆成功跳转到指定页面
                return redirect('/users/user_profile/')
            else:
                # 验证不通过提示！
                return HttpResponse("账号或者密码错误！")

    return render(request, 'login.html', {'form': form})


# 邮箱
class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 加密明文密码
                return user
        except Exception as e:
            return None


def active_user(request, active_code):
    """查询验证码"""
    print(active_code)
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    print(all_records)
    if all_records:
        for record in all_records:
            email = record.email
            print(email)
            user = User.objects.get(email=email)
            print(user)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse('链接有误！')
    return redirect('/users/login/')


def user_register(request):
    # 注册
    if request.method != 'POST':
        form = RegisterForm()
    # 处理填写好的表单，注册新用户，然后重定向到主页
    else:
        form = RegisterForm(request.POST)  # 【注意】这里的request.POST是一个字典，里面包含了用户提交的所有数据，包括用户名、邮箱和密码
        if form.is_valid():  # 如果提交的数据合法
            new_user = form.save(commit=False)  # 创建一个新用户对象，但暂时不保存到数据库
            new_user.set_password(form.cleaned_data['password'])  # 设置密码，这里的form.cleaned_data['password']是从表单中获取的密码
            new_user.username = form.cleaned_data.get('email')  # 将用户名设置为邮箱
            new_user.save()  # 保存到数据库
            # 注册成功，跳转到登录页面
            send_register_email(form.cleaned_data['email'], 'register')  # 发送邮件
            return redirect('/users/login/')
    return render(request, 'register.html', {'form': form})  # 注册页面


# 忘记密码
def forget_pwd(request):
    """ 找回密码 """
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            exists = User.objects.filter(email=email).exists()
            if exists:
                # 发送邮件
                send_register_email(email, 'forget')
                return redirect('/forget_pwd_url/', {'msg': '邮件已发送！'})
            else:
                return redirect('/users/register/', {'msg': '邮箱不存在！'})

    return render(request, 'forget_pwd.html', {'form': form})


# 重置密码
def forget_pwd_url(request, active_code):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('修改成功')
        else:
            return HttpResponse('修改失败')

    return render(request, 'reset_pwd.html', {'form': form})


# 用户个人中心

@login_required(login_url='users/login/')  # 设置登录后才能访问，如果没有登陆，就跳转到登录界面
def user_profile(request):
    user = User.objects.get(username=request.user)
    return render(request, 'user_profile.html', {'user': user})


# 登出
def logout_view(request):
    logout(request)
    return redirect('/users/login/')


# 编辑用户信息
@login_required(login_url='users:login')   # 登录之后允许访问
def editor_users(request):
    """ 编辑用户信息 """
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:   # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)       # 填充默认数据 当前用户
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()

                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单
    return render(request, 'editor_users.html', locals())
