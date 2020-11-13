# Create your models here.
from django.db import models
from appaccount.models import User
from datetime import datetime, date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.


class TeacherManager(models.Manager):
    # thuoc tinh cac de ket noi den DB
    def create(self, username, password, first_name, last_name, gender,
               birthday, email, phone_number, address, department):
        user = User(username=username, first_name=first_name, last_name=last_name, gender=gender,
                    birthday=birthday, email=email, phone_number=phone_number, address=address, is_teacher=True)
        user.set_password(password)
        user.save()
        teacher = Teacher(
            user=user,
            department=department,
        )
        teacher.save()
        return teacher


class StudentManager(models.Manager):
    def create(self, username, password, first_name, last_name, gender,
               birthday=None, email='', phone_number='', address='', is_crew=0, classes=None, course_year=None):
        user = User(username=username, first_name=first_name, last_name=last_name, gender=gender,
                    birthday=birthday, email=email, phone_number=phone_number, address=address)
        user.set_password(password)
        user.save()
        student = Student(
            user=user,
            is_crew=is_crew,
            classes=classes,
            course_year=course_year
        )
        student.save()
        return student


class Department(models.Model):  # bo mon, bo phan, to^~ nao
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    introduction = models.TextField(default='', null=True, blank=True)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return str(self.department_name)


class Teacher(models.Model):  # Giao vien
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING,
        related_name='teacher', null=True, blank=True)
    objects = TeacherManager()

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return str(self.user)


class SchoolYear(models.Model):  # Nam hoc
    id = models.BigAutoField(primary_key=True)
    from_year = models.DateField(default=date.today)
    to_year = models.DateField(default=date.today)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'schoolyear'

    def __str__(self):
        return str(self.from_year.year) + ' - ' + str(self.to_year.year)


class Classes(models.Model):  # Lop nao
    id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(null=False, max_length=10)  # vi du: A2
    course_year = models.IntegerField(
        default=date.today().year)

    class Meta:
        db_table = 'classes'
        constraints = [
            models.UniqueConstraint(
                fields=['class_name', 'course_year'], name='unique_classes')
        ]

    def __str__(self):
        return str(self.class_name)+' K_'+str(self.course_year)


class ActivitiesClass(models.Model):  # lop chu nhiem
    id = models.BigAutoField(primary_key=True)
    classes = models.ForeignKey(
        Classes, on_delete=models.DO_NOTHING, related_name='activities_class')  # id lop hoc
    form_teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING, related_name='activities_class')  # GV chu nhiem
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.DO_NOTHING, related_name='activities_class')

    class Meta:
        db_table = 'activitiesclass'
        constraints = [
            models.UniqueConstraint(
                fields=['classes', 'form_teacher', 'school_year'], name='unique_activitiesclass')
        ]

    def __str__(self):
        return str(self.classes)+' - '+str(self.form_teacher)


class Student(models.Model):  # Thong tin hoc sinh
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    is_crew = models.BooleanField(default=False, null=False, blank=False,
                                  choices=[(0, 'Chưa vào Đoàn'), (1, 'Đoàn viên')],)  # Doan vien
    course_year = models.IntegerField(
        default=date.today().year)  # khoa hoc, vidu:  K2008
    classes = models.ForeignKey(
        Classes, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='student')  # id lop hoc
    is_graduate = models.BooleanField(default=False, null=False, blank=False,
                                      choices=[(0, 'Chưa tốt nghiệp'), (1, 'Đã tốt nghiệp')],)
    objects = StudentManager()

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
    conduct_stsemester = models.IntegerField(null=True)  # hanh kiem hoc ky 1
    conduct_ndsemester = models.IntegerField(null=True)  # hanh kiem hoc ky 2
    conduct_gpasemester = models.IntegerField(null=True)  # hanh kiem ca nam
    rating = models.IntegerField(null=True)  # xep loai ca nam
    rating_stsemester = models.IntegerField(null=True)  # xep loai hoc ky 1
    rating_ndsemester = models.IntegerField(null=True)  # xep loai hoc ky 2

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
        return self.subject_name + ' - ' + str(self.grades)


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
    # time = models.IntegerField(null=True, blank=True)
    mid_stsemester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem giua ky 1 mon hoc
    end_stsemester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem cuoi ky 1 mon hoc
    gpa_stsemester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem trung binh ky 1 mon hoc
    mid_ndsemester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem giua ky 2 mon hoc
    end_ndsemester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem cuoi ky 2 mon hoc
    gpa_ndsemester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem trung binh ky 2 mon hoc
    gpa_year_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True)  # diem trung binh mon ca nam
    # true =cho hoc sinh xem y
    is_public = models.BooleanField(
        choices=[(0, 'NOT_PUBLIC'), (1, 'PUBLIC')], default=False)
    # false admin khong cho chinh sua diem
    is_locked = models.BooleanField(
        choices=[(0, 'UN_LOCKED'), (1, 'LOCKED')], default=False)
    due_input_st = models.DateField(default=date.today)  # han nhap diem
    due_input_nd = models.DateField(default=date.today)  # han nhap diem

    class Meta:
        db_table = 'marks'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'lecture', ], name='unique_student_lecture')
        ]

    def __str__(self):
        return str(self.student)


class MarksRegulary(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, related_name='marksregulary_student')
    marks_ref = models.ForeignKey(
        Marks, on_delete=models.DO_NOTHING, related_name='marksregulary',null=True,blank=True)
    semester = models.IntegerField(
        null=True, default=1)  # ma hoc ky, 1 hoac 2
    test_date = models.DateTimeField(default=timezone.now)
    times = models.IntegerField(null=True, default=1)
    point = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)
    note = models.CharField(max_length=200, default='', null=True)
    is_public = models.BooleanField(
        choices=[(0, 'NOT_PUBLIC'), (1, 'PUBLIC')], default=False)  # show diem
    is_locked = models.BooleanField(choices=[(0, 'UN_LOCKED'), (
        1, 'LOCKED')], default=False)  # admin khong cho chinh sua

    class Meta:
        db_table = 'marksregulary'

    def __str__(self):
        return str(self.point)
