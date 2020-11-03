# Create your models here.
from django.db import models
from appaccount.models import User
from datetime import datetime

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
    from_year = models.DateField()
    to_year = models.DateField()

    class Meta:
        db_table = 'schoolyear'

    def __str__(self):
        return str(self.from_year.year) + ' - ' + str(self.to_year.year)


class Classes(models.Model):  # Lop sinh hoat
    id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(null=False, max_length=10)
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.DO_NOTHING, related_name="classes")
    form_teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING)  # GV chu nhiem

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return str(self.class_name)


class Student(models.Model):  # Hoc sinh
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    is_crew = models.BooleanField(default=False)  # Doan vien

    class Meta:
        db_table = 'student'

    def __str__(self):
        return str(self.user)


class Conduct(models.Model):  # hoc sinh thuoc lop' hoc nao, hanh kiem
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    classes = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)
    conduct_stsemester = models.IntegerField(null=True)  # hanh kiem hoc ky 1
    conduct_ndsemester = models.IntegerField(null=True)  # hanh kiem hoc ky 2
    conduct_gpasemester = models.IntegerField(null=True)  # hanh kiem ca nam

    class Meta:
        db_table = 'conduct'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'classes'], name='unique_student_class')
        ]

    def __str__(self):
        return str(self.student)


class Subject(models.Model):  # cac mon hoc
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, null=True)
    level = models.CharField(max_length=10, default='')  # 10,11,12
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
    # classs = models.ForeignKey

    class Meta:
        db_table = 'lecture'
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'subject', 'classes'], name='unique_lecture')
        ]

    def __str__(self):
        return str(self.teacher) + ' - '+str(self.subject)


class Marks(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, related_name='marks')
    lecture = models.ForeignKey(
        Lecture, on_delete=models.DO_NOTHING, related_name='marks_lec')
    # school_year = models.ForeignKey(SchoolYear, on_delete=models.DO_NOTHING)
    mid_first_semester = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem giua ky 1
    end_first_semester = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem cuoi ky 1
    gpa_first_semester = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)  # diem trung binh ky 1
    mid_second_semester = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem giua ky 2
    end_second_semester = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem cuoi ky 2
    gpa_second_semester = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)  # diem trung binh ky 2
    gpa_year = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)  # diem trung binh ca nam
    is_public = models.BooleanField(default=False)  # khong hien diem
    is_locked = models.BooleanField(default=False)  # admin khong cho chinh sua

    class Meta:
        db_table = 'marks'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'lecture'], name='unique_student_lecture')
        ]

    def __str__(self):
        return str(self.student)


class MarksRegulary(models.Model):
    id = models.BigAutoField(primary_key=True)
    marks_ref = models.ForeignKey(
        Marks, on_delete=models.DO_NOTHING, related_name='marks_regulary')
    code_semester = models.IntegerField(null=True, default=1)
    test_date = models.DateTimeField()
    point = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    note = models.CharField(max_length=200, default='', null=True)
    is_public = models.BooleanField(default=False)  # show diem
    is_locked = models.BooleanField(default=False)  # admin khong cho chinh sua

    class Meta:
        db_table = 'marksregulary'

    def __str__(self):
        return str(self.point)
