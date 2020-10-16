# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from appaccount.models import User as CustomUser
from appmarks.models import Teacher, Student, Classes, Conduct, Department, Subject, SchoolYear, Marks, MarksRegulary, Lecture
from django.contrib.auth.forms import UserChangeForm
from appaccount.forms import CustomUserCreationForm
# Register your models here.


class CustomUserAdmin(BaseUserAdmin):
    # form = MyUserChangeForm
    model = CustomUser
    fieldsets = BaseUserAdmin.fieldsets + (
        ('More infor', {'fields': ('is_teacher',
                                   'gender', 'birthday', 'phone_number')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Classes)
admin.site.register(Lecture)
admin.site.register(Department)
admin.site.register(Conduct)
admin.site.register(Subject)
admin.site.register(SchoolYear)
admin.site.register(Marks)
admin.site.register(MarksRegulary)

# class AuthorAdmin(admin.ModelAdmin):
#     pass


# # class CustomUserAdmin(BaseUserAdmin):
# #     model = CustomUser
# #     add_form = CustomUserCreationForm
# #     form = CustomUserChangeForm
# #     # list_display = ['email', 'username', 'is_teacher','birthday']


# class TeacherInline(admin.StackedInline):
#     model = Teacher
#     can_delete = False
#     verbose_name_plural = 'Teacher'


# class StudentInline(admin.StackedInline):
#     model = Student
#     can_delete = False
#     verbose_name_plural = 'Student'

# # Define a new User admin


# class TeacherAdmin(BaseUserAdmin):
#     inlines = (TeacherInline,)


# class StudentAdmin(BaseUserAdmin):
#     inlines = (StudentInline,)


# # admin.site.unregister(User)
# admin.site.register(CustomUser, CustomUserAdmin)
# # admin.site.register(Teacher)
# # admin.site.register(Student)
