from django.urls import path

from users import admin, views
app_name='users'
urlpatterns = [
    path('login/', views.user_login,name='login'),  # 登录
    path('register/', views.user_register ,name='register'),  # 注册
    path('active/<active_code>/', views.active_user, name='active_user'),  # 激活用户
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),  # 忘记密码
    path('forget_pwd_url/<active_code>/', views.forget_pwd_url, name='forget_pwd_url'),  # 忘记密码
    path('user_profile/', views.user_profile, name='user_profile'),  # 用户个人信息
    path('logout/', views.logout_view, name='logout'),  # 登出
    path('editor_users/', views.editor_users, name='editor_users'),  # 编辑用户信息q
]