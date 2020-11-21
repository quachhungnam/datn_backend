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
                             LearningOutcomes, Department, Subject, SchoolYear, Marks, MarksRegulary, Lecture)
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

# STUDENT


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name = "Student ID"
    verbose_name_plural = 'Student Information'
    extra = 0


class StudentUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Student'


class StudentResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name',)

        # export_order = ()


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
                    'last_name', 'birthday', 'gender',  'email', 'get_course_year', 'get_classes', ]
    search_fields = ['class_name', ]
    list_filter = ('student__course_year',
                   'student__is_crew', 'student__is_graduate')
    odering = ['student__is_graduate']
    list_per_page = 50

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-data/', ImportData.as_view(), name='importdata'),
        ]
        return my_urls + urls

    def get_classes(self, CustomUser):
        return CustomUser.student.classes
    get_classes.short_description = 'Class'

    def get_course_year(self, CustomUser):
        return CustomUser.student.course_year
    get_course_year.short_description = 'CourseYear'

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_teacher=False, is_superuser=False, is_staff=False,
                                         is_active=True)

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
    verbose_name = 'Teacher ID'


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
                    'last_name', 'email', 'is_staff', 'get_department']

    def get_department(self, CustomUser):
        return CustomUser.teacher.department
    get_department.short_description = 'Department'

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_teacher=True, is_superuser=False, is_staff=False, is_active=True)

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

# DEPARTMENT


class TeacherInlineDepartment(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'List Teacher'
    verbose_name = 'Teacher'
    extra = 0
    readonly_fields = ['user']


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [TeacherInlineDepartment]
    list_display = ['department_name', 'count_teacher']
    search_fields = ['department_name', 'introduction']
    ordering = ['department_name']

    def count_teacher(self, Department):
        return Department.teacher.count()
    count_teacher.short_description = 'Quantum Teacher'

# CLASS


class StudentInlineClass(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'List Student'
    verbose_name = "Student ID"
    extra = 0


class ClassesAdmin(admin.ModelAdmin):
    inlines = [StudentInlineClass]
    list_display = ['class_name', 'course_year', 'count_student', ]
    search_fields = ['class_name', 'course_year', ]
    list_filter = ['course_year']
    ordering = ['course_year', 'class_name']
    list_per_page = 50

    def count_student(self, Classes):
        return Classes.student.count()
    count_student.short_description = 'Quantum Student'


class ActivitiesClassAdmin(admin.ModelAdmin):
    pass

# NAM HOC


class SchoolYearAdmin(admin.ModelAdmin):
    actions = ['set_LearningOutcomes']
    list_display = ['from_year', 'to_year', 'count_class']

    def count_class(self, SchoolYear):
        return SchoolYear.activities_class.count()
    count_class.short_description = 'Quantum class'

    def set_LearningOutcomes(self, request, queryset):
        print(queryset)
        students = Student.objects.filter(is_graduate=False)

        for school_year in queryset:
            for student in students:
                academic_record = LearningOutcomes(
                    student=student,
                    school_year=school_year
                )
                academic_record.save()
    set_LearningOutcomes.short_description = "Add new LearningOutcomes for all Student"


class SubjectAdmin(admin.ModelAdmin):
    pass

# LECTURE


# class StudentInlineLecture(admin.StackedInline):
#     model = Student
#     verbose_name_plural = 'List Student'
#     verbose_name = 'Student ID'
#     readonly_fields = ['user']

class MarksInlineLecture(admin.StackedInline):
    model = Marks
    verbose_name_plural = 'List Marks'
    vervose_name = 'Mark ID'
    extra = 0


class LectureAdmin(admin.ModelAdmin):
    inlines = [MarksInlineLecture]
    list_display = ['teacher', 'subject', 'classes', 'school_year']
    actions = ['add_marks_class']

    def add_marks_class(self, request, queryset):
        for lecture in queryset:
            print(lecture.classes)
            students = Student.objects.filter(
                is_graduate=False, classes=lecture.classes)

            for student in students:
                marks = Marks(
                    student=student,
                    lecture=lecture
                )
                marks.save()
    add_marks_class.short_description = "Add mark for all Student of lecture"


class LearningOutcomesAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_fullname', 'get_course_year', 'get_class', 'school_year',
                    'year_gpa', 'year_conduct', 'year_rating', ]
    list_select_related = ['student']
    ordering = ['school_year', 'student__classes', 'student', ]

    def get_fullname(self, LearningOutcomes):
        return LearningOutcomes.student.user.first_name+' '+LearningOutcomes.student.user.last_name
    get_fullname.short_description = 'FULL NAME'

    def get_class(self, LearningOutcomes):
        return LearningOutcomes.student.classes.class_name
    get_class.short_description = 'Classes'

    def get_course_year(self, LearningOutcomes):
        return LearningOutcomes.student.course_year
    get_course_year.short_description = 'course year'

    pass


class MarksAdmin(admin.ModelAdmin):
    pass


class MarksRegularyAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentUser, StudentAdmin)
admin.site.register(TeacherUser, TeacherAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(ActivitiesClass, ActivitiesClassAdmin)
admin.site.register(LearningOutcomes, LearningOutcomesAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(Marks, MarksAdmin)
admin.site.register(MarksRegulary, MarksRegularyAdmin)
