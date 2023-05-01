from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, EmailVerifyRecord

# Register your models here.

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户信息'


class UserAdmin(UserAdmin):
    inlines = [UserProfileInline]


admin.site.register(User, UserAdmin)


@admin.register(EmailVerifyRecord)
class EamilVerifyRecordAdmin(admin.ModelAdmin):
    '''Admin View for EamilVerifyRecord'''

    list_display = ('code',)
