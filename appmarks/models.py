# Create your models here.
from django.db import models
from appaccount.models import User
from datetime import datetime

# Create your models here.


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    introduction = models.TextField(default='')


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    deparment = models.ForeignKey(Department, on_delete=models.DO_NOTHING)


class Classes(models.Model):
    id = models.BigAutoField(primary_key=True)
    classes_name = models.CharField(null=False, max_length=10)
    form_teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING)  # Giao vien chu nhiem
    school_year = models.CharField(null=False, max_length=10)


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    classes = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)


class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    descriptions = models.TextField(default='', null=True)


class Marks(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    semester = models.CharField(max_length=5)  # hoc ky nam hoc
    school_year = models.CharField(max_length=10)
    half_test = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem giua ky
    end_test = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem cuoi ky
    everage_test = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)  # diem trung binh mon


class MarksRegulary(models.Model):
    id = models.BigAutoField(primary_key=True)
    marks_id = models.ForeignKey(Marks, on_delete=models.DO_NOTHING)
    test_date = models.DateTimeField()
    marks = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    note = models.CharField(max_length=200, default='', null=True)
