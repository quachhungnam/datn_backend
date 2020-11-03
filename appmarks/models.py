# Create your models here.
from django.db import models
from appaccount.models import User
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Department(models.Model):  # bo mon, bo phan, to^~ nao
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    introduction = models.TextField(default='')

    class Meta:
        db_table = 'department'

    def __str__(self):
        return str(self.department_name)


class Teacher(models.Model):  # Giao vien
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, related_name='teacher')

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return str(self.user)


class SchoolYear(models.Model):  # Nam hoc
    id = models.BigAutoField(primary_key=True)
    from_year = models.DateField(null=True)
    to_year = models.DateField(null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'schoolyear'

    def __str__(self):
        return str(self.from_year.year) + ' - ' + str(self.to_year.year)


class Classes(models.Model):  # Lop sinh hoat
    id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(null=False, max_length=10)  # vi du: A2
    course_year = models.DateField(null=True)  # khoa hoc, vidu:  K2008

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return str(self.class_name)


class ActivitiesClass(models.Model):  # lop sinh hoat,
    id = models.BigAutoField(primary_key=True)
    classes = models.ForeignKey(
        Classes, on_delete=models.DO_NOTHING)  # id lop hoc
    form_teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING)  # GV chu nhiem
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.DO_NOTHING, related_name='activities_class')

    class Meta:
        db_table = 'activitiesclass'

    # def __str__(self):
    #     return str(self.class_name)


class Student(models.Model):  # Thong tin hoc sinh
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    is_crew = models.BooleanField(default=False)  # Doan vien
    classes = models.ForeignKey(
        Classes, on_delete=models.DO_NOTHING)  # id lop hoc

    class Meta:
        db_table = 'student'

    def __str__(self):
        return str(self.user)


class AcademicRecord(models.Model):  # ket qua hoc tap va ren luyen theo nam hoc
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.DO_NOTHING, related_name='academic_record')
    gpa_first_semester = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)  # diem trung binh tat ca mon hk1
    gpa_second_semester = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)  # diem trung binh tat ca mon hk2
    gpa_year = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)  # diem trung binh ca nam hoc
    # hanh kiem hoc ky 1 1,2,3,4,5 tuong ung voi kem,yeu,tb,kha, tot
    conduct_stsemester = models.IntegerField(null=True)
    conduct_ndsemester = models.IntegerField(null=True)  # hanh kiem hoc ky 2
    conduct_gpasemester = models.IntegerField(null=True)  # hanh kiem ca nam
    rating = models.IntegerField(null=True)

    class Meta:
        db_table = 'academicrecord'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'school_year'], name='unique_student_school_year')
        ]

    def __str__(self):
        return str(self.student)


class Subject(models.Model):  # cac mon hoc
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, null=True)
    grades = models.IntegerField(choices=[(10, 'Grades 10'), (11, 'Grades 11'), (12, 'Grades 12')],
                                 validators=[MinValueValidator(10), MaxValueValidator(12)])  # lop 10,11,12
    descriptions = models.TextField(default='', null=True)

    class Meta:
        db_table = 'subject'

    def __str__(self):
        return self.subject_name + ' - '+self.level


class Lecture(models.Model):  # Giao vien day nhung mon nao
    id = models.BigAutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    classes = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.DO_NOTHING, related_name='lecture')
    status = models.BooleanField(default=True)
    # classs = models.ForeignKey

    class Meta:
        db_table = 'lecture'
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'subject', 'classes', 'school_year'], name='unique_lecture')
        ]

    def __str__(self):
        return str(self.teacher) + ' - '+str(self.subject)


class Marks(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, related_name='marks_student')
    lecture = models.ForeignKey(
        Lecture, on_delete=models.DO_NOTHING, related_name='marks_lecture')
    semester = models.IntegerField(null=True, default=1)  # ma hoc ky, 1 hoac 2
    # time = models.IntegerField(null=True, blank=True)
    mid_semester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem giua ky mon hoc
    end_semester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem cuoi ky mon hoc
    gpa_semester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem trung binh ky mon hoc
    gpa_year_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem trung binh mon ca nam
    # true =cho hoc sinh xem diem
    is_public = models.BooleanField(
        choices=[(0, 'NOT_PUBLIC'), (1, 'PUBLIC')], default=False)
    # false admin khong cho chinh sua diem
    is_locked = models.BooleanField(
        choices=[(0, 'UN_LOCKED'), (1, 'LOCKED')], default=False)
    due_input = models.DateField()  # han nhap diem

    class Meta:
        db_table = 'marks'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'lecture', 'semester'], name='unique_student_lecture_semester')
        ]

    def __str__(self):
        return str(self.student)


class MarksRegulary(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, related_name='marksregulary_student')
    lecture = models.ForeignKey(
        Lecture, on_delete=models.DO_NOTHING, related_name='marksregulary_lecture')
    semester = models.IntegerField(null=True, default=1)  # ma hoc ky, 1 hoac 2
    test_date = models.DateTimeField()
    times = models.IntegerField(null=True, default=1)
    point = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    note = models.CharField(max_length=200, default='', null=True)
    is_public = models.BooleanField(
        choices=[(0, 'NOT_PUBLIC'), (1, 'PUBLIC')], default=False)  # show diem
    is_locked = models.BooleanField(choices=[(0, 'UN_LOCKED'), (
        1, 'LOCKED')], default=False)  # admin khong cho chinh sua

    class Meta:
        db_table = 'marksregulary'

    def __str__(self):
        return str(self.point)
