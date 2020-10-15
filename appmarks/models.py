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
        db_table = 'deparment'


class Teacher(models.Model):  # Giao vien
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    deparment = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'teacher'


class SchoolYear(models.Model):  # Nam hoc
    id = models.BigAutoField(primary_key=True)
    from_year = models.DateField()
    to_year = models.DateField()

    class Meta:
        db_table = 'schoolyear'


class Classes(models.Model):  # Lop sinh hoat
    id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(null=False, max_length=10)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.DO_NOTHING)
    form_teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING)  # GV chu nhiem

    class Meta:
        db_table = 'classes'


class Student(models.Model):  # Hoc sinh
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    is_crew = models.BooleanField(default=False)  # Doan vien

    class Meta:
        db_table = 'student'


class Conduct(models.Model):  # hoc sinh thuoc lop' hoc nao, hanh kiem
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    classes = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)
    conduct_stsemester = models.IntegerField()  # hanh kiem hoc ky 1
    conduct_ndsemester = models.IntegerField()  # hanh kiem hoc ky 2
    conduct_gpasemester = models.IntegerField()  # hanh kiem ca nam

    class Meta:
        db_table = 'conduct'


class Subject(models.Model):  # cac mon hoc
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, null=True)
    level = models.CharField(max_length=10, default='')  # 10,11,12
    descriptions = models.TextField(default='', null=True)

    class Meta:
        db_table = 'subject'


class Lecture(models.Model):  # Giao vien day nhung mon nao
    id = models.BigAutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    classes = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'lecture'


# class LectureClass(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     lecture = models.ForeignKey(Lecture, on_delete=models.DO_NOTHING)
#     classes = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)

#     class Meta:
#         db_table = 'lectureclass'


class Marks(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    lecture = models.ForeignKey(
        Lecture, on_delete=models.DO_NOTHING)
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


class MarksRegulary(models.Model):
    id = models.BigAutoField(primary_key=True)
    marks_ref = models.ForeignKey(Marks, on_delete=models.DO_NOTHING)
    test_date = models.DateTimeField()
    point = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    note = models.CharField(max_length=200, default='', null=True)
    is_public = models.BooleanField(default=False)  # show diem
    is_locked = models.BooleanField(default=False)  # admin khong cho chinh sua

    class Meta:
        db_table = 'marksregulary'

# class Department(models.Model):  # Bo mon, bo phan
#     id = models.AutoField(primary_key=True)
#     department_name = models.CharField(max_length=100)
#     introduction = models.TextField(default='')


# class SchoolYear(models.Model):  # Nam hoc
#     id = models.BigAutoField(primary_key=True)
#     start_year = models.CharField(max_length=4)
#     end_year = models.CharField(max_length=4)


# class Teacher(models.Model):  # Giao vien
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, primary_key=True)
#     deparment = models.ForeignKey(Department, on_delete=models.DO_NOTHING)


# class Classes(models.Model):  # Lop sinh hoat
#     id = models.BigAutoField(primary_key=True)
#     classes_name = models.CharField(null=False, max_length=10)
#     form_teacher = models.ForeignKey(
#         Teacher, on_delete=models.DO_NOTHING)  # Giao vien chu nhiem
#     school_year = models.CharField(null=False, max_length=10)


# class Student(models.Model):  # Hoc sinh
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, primary_key=True)
#     classes = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)


# class Conduct(models.Model):  # Hanh kiem
#     id = models.BigAutoField(primary_key=True)
#     student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
#     shoolyear = models.ForeignKey(SchoolYear, on_delete=models.DO_NOTHING)
#     semester_first = models.IntegerField()
#     semester_second = models.IntegerField()


# class Lecture(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     teacher_id = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
#     pass


# class DGTX(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     pass


# class Semester(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     schoolyear = models.ForeignKey(SchoolYear, on_delete=models.DO_NOTHING)
#     semester_name = models.CharField(max_length=10)
#     start_week = models.CharField(max_length=3)
#     end_week = models.IntegerField(max_length=3)
#     pass


# class Subject(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     subject_name = models.CharField(max_length=50, null=True)
#     # teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
#     descriptions = models.TextField(default='', null=True)


# class Marks(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
#     subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
#     semester = models.CharField(max_length=5)  # hoc ky nam hoc
#     school_year = models.CharField(max_length=10)
#     half_test = models.DecimalField(
#         max_digits=3, decimal_places=1, null=True)  # diem giua ky
#     end_test = models.DecimalField(
#         max_digits=3, decimal_places=1, null=True)  # diem cuoi ky
#     everage_test = models.DecimalField(
#         max_digits=3, decimal_places=1, default=0.0)  # diem trung binh mon


# class MarksRegulary(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     marks_id = models.ForeignKey(Marks, on_delete=models.DO_NOTHING)
#     test_date = models.DateTimeField()
#     marks = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
#     note = models.CharField(max_length=200, default='', null=True)
