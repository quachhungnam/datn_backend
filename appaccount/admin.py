# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from appaccount.models import User as CustomUser
from appmarks.models import Teacher, Student, Classes, Conduct, Department, Subject, SchoolYear, Marks, MarksRegulary, Lecture
from django.contrib.auth.forms import UserChangeForm
from appaccount.forms import CustomUserCreationForm
from django.shortcuts import render
from django.utils.translation import ngettext
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from appmarks.models import Student, Teacher, Lecture, Classes, Marks
# Register your models here.


class CustomUserAdmin(BaseUserAdmin):
    # form = MyUserChangeForm
    model = CustomUser
    fieldsets = BaseUserAdmin.fieldsets + (
        ('More infor', {'fields': ('is_teacher',
                                   'gender', 'birthday', 'phone_number', 'address')}),
    )
    actions = ['set_is_teacher', 'set_user_student']
    list_display = ['username', 'first_name',
                    'last_name', 'email', 'is_staff', 'is_teacher']

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


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_fullname',
                    'get_gender', 'get_birthday', 'is_crew', ]
    search_fields = ['user__username']
    actions = ['add_student_class']

    def get_fullname(self, Student):
        return Student.user.first_name + ' ' + Student.user.last_name
    get_fullname.short_description = 'fullname'

    def get_gender(self, Student):
        if(Student.user.gender):
            return 'Nam'

        if Student.user.gender == 0:
            return 'Nữ'
        return '--'
    get_gender.short_description = 'gender'

    def get_birthday(self, Student):
        return Student.user.birthday
    get_birthday.short_description = 'birthday'

    def add_student_class(self, request, queryset):
        # return render(request,
        #               'admin/order_intermediate.html',)
        all_class = Classes.objects.all()
        print(all_class)
        print(request.POST)
        if 'apply' in request.POST:
            class_id = request.POST.get('setclass')
            # print(class_id)
            print('ddd')
            for student in queryset:
                conduct = Student.objects.create(
                    student=student, classes=class_id)
            self.message_user(request,
                              "Add student {} to class".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request,
                      'admin/selectclass.html',
                      context={'students': queryset, 'all_class': all_class})

    add_student_class.short_description = "Add student to Class"

    #               context={})
    # for user in (queryset):
    #     student = Student.objects.create(user=user)
    # self.message_user(request, ngettext(
    #     '%d user is seted to Student.',
    #     '%d users is seted to Student.',
    #     student,
    # ) % student, messages.SUCCESS)


class TeacherAdmin(admin.ModelAdmin):

    list_display = ['user', 'get_fullname',
                    'get_gender', 'get_birthday', 'department', 'get_phone', 'get_address']
    ordering = ['user']

    def get_fullname(self, Teacher):
        return Teacher.user.first_name + ' ' + Teacher.user.last_name
    get_fullname.short_description = 'fullname'

    def get_gender(self, Teacher):
        if(Teacher.user.gender):
            return 'Nam'

        if Teacher.user.gender == 0:
            return 'Nữ'
        return '--'
    get_gender.short_description = 'gender'

    def get_birthday(self, Teacher):
        return Teacher.user.birthday
    get_birthday.short_description = 'birthday'

    def get_phone(self, Teacher):
        return Teacher.user.phone_number
    get_phone.short_description = 'mobile'

    def get_address(self, Teacher):
        return Teacher.user.address
    get_address.short_description = 'address'


class ClassesAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'school_year',
                    'form_teacher', 'get_fullname']
    list_filter = ('class_name', 'school_year', 'form_teacher')
    search_fields = ['class_name', 'school_year__from_year',
                     'form_teacher__user__username']
    ordering = ['class_name']

    def get_fullname(self, Classes):
        return Classes.form_teacher.user.first_name + ' ' + Classes.form_teacher.user.last_name
    get_fullname.short_description = 'fullname'


class LectureAdmin(admin.ModelAdmin):
    list_display = ['classes', 'subject',
                    'teacher', 'fullname', 'get_schoolyear']
    ordering = ['classes']
    list_filter = ['classes', 'subject', 'teacher']

    def fullname(self, Lecture):
        return Lecture.teacher.user.first_name + ' ' + Lecture.teacher.user.last_name
    fullname.short_description = 'fullname'

    def get_schoolyear(self, Lecture):
        return str(Lecture.classes.school_year.from_year.year) + ' - ' + str(Lecture.classes.school_year.to_year.year)
    get_schoolyear.short_description = 'School Year'

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            pass
        else:
            # do your own custom code
            pass
        obj.save()
        students = Student.objects.all().filter(conduct__classes=obj.classes)
        for student in students:
            mark = Marks(student=student, lecture=obj)
            mark.save()


class ConductAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_fullname', 'classes', 'get_schoolyear']
    list_filter = ('classes', 'conduct_gpasemester',)
    search_fields = ['student__user__username',
                     'student__user__first_name', 'student__user__last_name', ]
    ordering = ['classes']

    def get_fullname(self, Conduct):
        return Conduct.student.user.first_name + ' ' + Conduct.student.user.last_name
    get_fullname.short_description = 'fullname'

    def get_schoolyear(self, Conduct):
        return Conduct.classes.school_year
    get_schoolyear.short_description = 'schoolyear'


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'level', 'descriptions']
    list_filter = ('subject_name', 'level')
    ordering = ['level']


class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_fullname', 'get_classes',
                    'get_subjectname', 'gpa_year']
    list_filter = ('student', 'lecture')
    # ho ten

    def get_fullname(self, Marks):
        return Marks.student.user.first_name + ' ' + Marks.student.user.last_name
    get_fullname.short_description = 'fullname'

    def get_classes(self, Marks):
        return Marks.lecture.classes
    get_classes.short_description = 'Class'

    def get_subjectname(self, Marks):
        return Marks.lecture.subject
    get_subjectname.short_description = 'subject'


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_name']


class MarksRegularyAdmin(admin.ModelAdmin):
    list_display = ['marks_ref','test_date',
                    'point', 'note', 'is_public', 'is_locked']

    # ordering = ['level']
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Conduct, ConductAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SchoolYear)
admin.site.register(Marks, MarksAdmin)
admin.site.register(MarksRegulary, MarksRegularyAdmin)

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
