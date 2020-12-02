# Create your models here.
from django.db import models
from appaccount.models import User
from datetime import datetime, date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from ckeditor.fields import RichTextField

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
    def create(self, username, password, first_name, last_name, gender=None,
               birthday=None, email='', phone_number='', address='', classes=None, course_year=None):
        user = User(username=username, first_name=first_name, last_name=last_name, gender=gender,
                    birthday=birthday, email=email, phone_number=phone_number, address=address)
        user.set_password(password)
        user.save()
        student = Student(
            user=user,
            classes=classes,
            course_year=course_year
        )
        student.save()
        return student


class Department(models.Model):  # bo mon, bo phan, to^~ nao
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(
        default='', null=True, blank=True, max_length=100)
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
    from_year = models.IntegerField(default=date.today().year)
    to_year = models.IntegerField(default=date.today().year+1)

    class Meta:
        db_table = 'schoolyear'

    def __str__(self):
        return str(self.from_year) + ' - ' + str(self.to_year)


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


class AdminClass(models.Model):  # lop chu nhiem
    id = models.BigAutoField(primary_key=True)
    classes = models.ForeignKey(
        Classes, on_delete=models.DO_NOTHING, related_name='activities_class')  # id lop hoc
    admin_teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING, related_name='activities_class')  # GV chu nhiem
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.DO_NOTHING, related_name='activities_class')

    class Meta:
        db_table = 'adminclass'
        constraints = [
            models.UniqueConstraint(
                fields=['classes', 'admin_teacher', 'school_year'], name='unique_adminclass')
        ]

    def __str__(self):
        return str(self.classes)+' - '+str(self.admin_teacher)


class Student(models.Model):  # Thong tin hoc sinh
    # CREW_CHOICES = [(0, 'Chưa vào Đoàn'), (1, 'Đoàn viên')]
    GRADUATE_CHOICES = [(0, 'Chưa tốt nghiệp'), (1, 'Đã tốt nghiệp')]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    classes = models.ForeignKey(
        Classes, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='student')  # id lop hoc
    # is_crew = models.BooleanField(default=False, null=False, blank=False,
    #                               choices=CREW_CHOICES)  # Doan vien
    course_year = models.IntegerField(
        default=date.today().year)  # khoa hoc, vidu:  K2008

    is_graduate = models.BooleanField(default=False, null=False, blank=False,
                                      choices=GRADUATE_CHOICES)
    objects = StudentManager()

    class Meta:
        db_table = 'student'

    def __str__(self):
        return str(self.user)

# ket qua hoc tap va ren luyen theo nam hoc


class LearningOutcomes(models.Model):
    RATING_CHOICES = [
        (0, 'Kém'), (1, 'Yếu'),
        (2, 'Trung bình'), (3, 'Khá'), (4, 'Giỏi')]
    CONDUCT_CHOICES = [
        (1, 'Yếu'), (2, 'Trung bình'), (3, 'Khá'), (4, 'Tốt')
    ]
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.DO_NOTHING, related_name='learningoutcomes')
    # st_semester_gpa = models.DecimalField(
    #     max_digits=3, decimal_places=1, default=0.0)  # diem trung binh tat ca mon hk1
    # nd_semester_gpa = models.DecimalField(
    #     max_digits=3, decimal_places=1, default=0.0)  # diem trung binh tat ca mon hk2
    # year_gpa = models.DecimalField(
    #     max_digits=3, decimal_places=1, default=0.0)  # diem trung binh ca nam hoc

    # Xep loai hanh kiem 1,2,3,4
    st_semester_conduct = models.IntegerField(
        null=True, blank=True, choices=CONDUCT_CHOICES)  # hanh kiem hoc ky 1
    nd_semester_conduct = models.IntegerField(
        null=True, blank=True, choices=CONDUCT_CHOICES)  # hanh kiem hoc ky 2
    # year_conduct = models.IntegerField(
    #     null=True, blank=True, choices=CONDUCT_CHOICES)  # hanh kiem ca nam

    # st_semester_rating = models.IntegerField(
    #     null=True, blank=True, choices=RATING_CHOICES)  # xep loai hoc ky 1
    # nd_semester_rating = models.IntegerField(
    #     null=True, blank=True, choices=RATING_CHOICES)  # xep loai hoc ky 2
    # year_rating = models.IntegerField(
    #     null=True, blank=True, choices=RATING_CHOICES)  # xep loai ca nam

    class Meta:
        db_table = 'learningoutcomes'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'school_year'], name='unique_learningoutcomes')
        ]

    def __str__(self):
        return str(self.student)


class Subject(models.Model):  # cac mon hoc
    GRADES_CHOICE = [(10, 'Lớp 10'), (11, 'Lớp 11'), (12, 'Lớp 12')]
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(
        default='', null=True, blank=True, max_length=50)
    grades = models.IntegerField(choices=GRADES_CHOICE,
                                 validators=[MinValueValidator(10), MaxValueValidator(12)])
    descriptions = models.TextField(default='', null=True, blank=True)

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
    st_due_input = models.DateField(
        default=date.today, null=True, blank=True)  # han nhap diem
    nd_due_input = models.DateField(
        default=date.today, null=True, blank=True)  # han nhap diem

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

    mid_st_semester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)  # diem giua ky 1 mon hoc
    end_st_semester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)  # diem cuoi ky 1 mon hoc
    # gpa_st_semester_point = models.DecimalField(
    #     max_digits=3, decimal_places=1, null=True, blank=True)  # diem trung binh ky 1 mon hoc

    mid_nd_semester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)  # diem giua ky 2 mon hoc
    end_nd_semester_point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)  # diem cuoi ky 2 mon hoc
    # gpa_nd_semester_point = models.DecimalField(
    #     max_digits=3, decimal_places=1, null=True, blank=True)  # diem trung binh ky 2 mon hoc

    # gpa_year_point = models.DecimalField(
    #     max_digits=3, decimal_places=1, null=True, blank=True)  # diem trung binh mon ca nam

    # true =cho hoc sinh xem y
    is_public = models.BooleanField(
        choices=[(0, 'NOT_PUBLIC'), (1, 'PUBLIC')], default=False)
    # false admin khong cho chinh sua diem
    is_locked = models.BooleanField(
        choices=[(0, 'UN_LOCKED'), (1, 'LOCKED')], default=False)

    # st_due_input = models.DateField(
    #     default=date.today, null=True, blank=True)  # han nhap diem
    # nd_due_input = models.DateField(
    #     default=date.today, null=True, blank=True)  # han nhap diem

    class Meta:
        db_table = 'marks'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'lecture', ], name='unique_student_lecture')
        ]

    def __str__(self):
        return str(self.student)+' - '+str(self.lecture.subject.subject_name)


class MarksRegulary(models.Model):
    CHOICES_SEMESTER = [(1, 'Học kỳ 1'), (2, 'Học kỳ 2')]
    id = models.BigAutoField(primary_key=True)
    marks_ref = models.ForeignKey(
        Marks, on_delete=models.DO_NOTHING, related_name='marksregulary', null=True, blank=True)
    semester = models.IntegerField(choices=CHOICES_SEMESTER, validators=[
                                   MinValueValidator(1), MaxValueValidator(2)])  # ma hoc ky, 1 hoac 2
    # test_date = models.DateTimeField(
    #     default=timezone.now, null=True, blank=True)
    input_date = models.DateTimeField(
        default=timezone.now, null=True, blank=True)
    # times = models.IntegerField(null=True, blank=True)
    point = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    note = models.CharField(default='', null=True,
                            blank=True, max_length=200, )
    # is_public = models.BooleanField(
    #     choices=[(0, 'NOT_PUBLIC'), (1, 'PUBLIC')], default=False)  # show diem
    # is_locked = models.BooleanField(choices=[(0, 'UN_LOCKED'), (
    #     1, 'LOCKED')], default=False)  # admin khong cho chinh sua

    class Meta:
        db_table = 'marksregulary'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['marks_ref', 'semester'], name='unique_marksregulary')
        # ]

    def __str__(self):
        return str(self.point)


class Notice(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        default='', null=True, blank=True, max_length=200)
    post_date = models.DateTimeField(
        default=timezone.now, null=True, blank=True)
    content = RichTextField()

    class Meta:
        db_table = 'notice'

    def __str__(self):
        return self.title
