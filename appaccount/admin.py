# from django.contrib import admin

# Register your models here.
import pandas as pd
from pandas import ExcelFile
from django.shortcuts import redirect
import csv
from django.urls import include, path
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.admin import ImportExportMixin, ImportMixin
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from appaccount.forms import CustomUserCreationForm
from django.shortcuts import render
from django.utils.translation import ngettext
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from appaccount.models import User as CustomUser
from appmarks.models import (Teacher, Student, Classes, ActivitiesClass,
                             AcademicRecord, Department, Subject, SchoolYear, Marks, MarksRegulary, Lecture)
from import_export.widgets import ForeignKeyWidget
from appmarks.views import ImportData
# Register your models here.
# SET Header and Title
admin.site.site_header = 'Management School Administration'
admin.site.site_title = 'Management School'
admin.site.index_title = 'Management School'
# USER


class CustomUserAdmin(BaseUserAdmin):
    # form = MyUserChangeForm
    model = CustomUser
    fieldsets = BaseUserAdmin.fieldsets + (
        ('More infor', {'fields': ('is_teacher',
                                   'gender', 'birthday', 'phone_number', 'address')}),
    )
    # actions = ['set_is_teacher', 'set_user_student']
    list_display = ['username', 'first_name',
                    'last_name', 'email', 'is_staff', 'is_teacher']
    list_per_page = 50

    def set_is_teacher(self, request, queryset):
        updated = queryset.update(is_teacher=True)
        # for user in queryset:
        #     teacher = Teacher.objects.create(user=user)
        self.message_user(request, ngettext(
            '%d user is seted to Teacher.',
            '%d users is seted to Teacher.',
            updated,
        ) % updated, messages.SUCCESS)
    set_is_teacher.short_description = "Set user is Teacher"

    def set_user_student(self, request, queryset):
        for user in (queryset):
            student = Student.objects.create(user=user)
        self.message_user(request, ngettext(
            '%d user is seted to Student.',
            '%d users is seted to Student.',
            student,
        ) % student, messages.SUCCESS)
    set_user_student.short_description = "Set user is Student"

    def save_model(self, request, obj, form, change):
        # obj.added_by = request.user
        print('save user from import')
        super().save_model(request, obj, form, change)


# STUDENT

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Information'


class StudentUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Student'


class StudentResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name',)

        # export_order = ()


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class StudentAdmin(ImportExportActionModelAdmin, BaseUserAdmin):
    model = Student
    resource_class = StudentResource
    change_list_template = "admin/changelist_student.html"
    inlines = (StudentInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name',
                                        'gender', 'birthday', 'address', 'phone_number', 'email')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff',),
        }),
    )
    list_display = ['username', 'first_name',
                    'last_name', 'email', 'get_classes', 'get_course_year', ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-data/', ImportData.as_view(), name='importdata'),
        ]
        return my_urls + urls

    # def import_csv(self, request):
    #     if request.method == "POST":
    #         csv_file = request.FILES["csv_file"]
    #         # reader = csv.reader(csv_file)
    #         df = pd.read_excel(csv_file, sheet_name=0, index_col=0)
    #         print(df)
    #         # print(reader)
    #         # Create Hero objects from passed in data
    #         # ...
    #         self.message_user(request, "Your csv file has been imported")
    #         return redirect("..")
    #     form = CsvImportForm()
    #     payload = {"form": form}
    #     return render(
    #         request, "admin/csv_form.html", payload
    #     )

    def get_classes(self, CustomUser):
        return CustomUser.student.classes
    get_classes.short_description = 'Class'

    def get_course_year(self, CustomUser):
        return CustomUser.student.course_year
    get_course_year.short_description = 'CourseYear'
    list_filter = ('student__course_year', 'student__is_crew',)

    list_per_page = 50
#     search_fields = ['class_name', 'school_year__from_year',
#                      'form_teacher__user__username']

    def get_queryset(self, request):
        # return Student.objects.select_related('user').all()
        return CustomUser.objects.filter(is_teacher=False, is_superuser=False)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        obj = form.instance
        if change == False:
            student = Student(user=obj)
            student.save()
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)

# TEACHER


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Information'


class TeacherUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Teacher'


class TeacherAdmin(BaseUserAdmin):
    model = Teacher
    inlines = (TeacherInline,)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name',
                                        'gender', 'birthday', 'address', 'phone_number', 'email')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff',),
        }),
    )
    list_display = ['username', 'first_name',
                    'last_name', 'email', 'is_staff']

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_teacher=True, is_superuser=False)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.is_teacher = True
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        obj = form.instance
        if change == False:
            teacher = Teacher(user=obj)
            teacher.save()
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)


class DepartmentAdmin(admin.ModelAdmin):
    pass


class ClassesAdmin(admin.ModelAdmin):
    pass


class ActivitiesClassAdmin(admin.ModelAdmin):
    pass


class SchoolYearAdmin(admin.ModelAdmin):
    pass


class SubjectAdmin(admin.ModelAdmin):
    pass


class LectureAdmin(admin.ModelAdmin):
    pass


class AcademicRecordAdmin(admin.ModelAdmin):
    pass


class MarksAdmin(admin.ModelAdmin):
    pass


class MarksRegularyAdmin(admin.ModelAdmin):
    pass


class StudentUser2(Student):
    class Meta:
        proxy = True
        verbose_name = 'Student'


class UserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'Student Information'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentUser, StudentAdmin)
admin.site.register(TeacherUser, TeacherAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(ActivitiesClass, ActivitiesClassAdmin)
admin.site.register(AcademicRecord, AcademicRecordAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(Marks, MarksAdmin)
admin.site.register(MarksRegulary, MarksRegularyAdmin)
