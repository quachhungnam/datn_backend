from rest_framework import serializers
from appmarks.models import (Department, Teacher, SchoolYear, Classes, Student,
                             Subject, Lecture, Marks, MarksRegulary,
                             AdminClass, LearningOutcomes,
                             Notice)
from appaccount.serializiers import (UserSerializer, UserSerializerForMarks)
from appaccount.models import User
from django.db import models


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'introduction']
        read_only_fields = ['id']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'department']

    def create(self, validated_data):
        return Teacher.objects.create(
            username=validated_data['user']['username'],
            password=validated_data['user']['password'],
            first_name=validated_data.get('user').get('first_name', ''),
            last_name=validated_data['user'].get('last_name', ''),
            gender=validated_data['user'].get('gender'),
            birthday=validated_data['user'].get('birthday'),
            email=validated_data['user'].get('email', ''),
            phone_number=validated_data['user'].get('phone_number', ''),
            address=validated_data['user'].get('address', ''),
            department=validated_data.get('department')
        )


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = ['id', 'from_year', 'to_year']
        read_only_fields = ['id']


class ClassesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classes
        fields = ['id', 'class_name', 'course_year']
        read_only_fields = ['id']


class AdminClassSerializer(serializers.ModelSerializer):
    classes = ClassesSerializer()
    school_year = SchoolYearSerializer()

    class Meta:
        model = AdminClass
        fields = ['id', 'classes', 'admin_teacher', 'school_year']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    classes = ClassesSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['user', 'classes', 'course_year', 'is_graduate']
        read_only_fields = ['course_year', 'is_graduate']

    def create(self, validated_data):
        return Student.objects.create(
            username=validated_data['user']['username'],
            password=validated_data['user']['password'],
            first_name=validated_data.get('user').get('first_name', ''),
            last_name=validated_data['user'].get('last_name', ''),
            gender=validated_data['user'].get('gender'),
            birthday=validated_data['user'].get('birthday'),
            email=validated_data['user'].get('email', ''),
            phone_number=validated_data['user'].get('phone_number', ''),
            address=validated_data['user'].get('address', ''),
            classes=validated_data.get('classes'),
            # is_crew=validated_data.get('is_crew', False),
        )


class LearningOutcomesSerializer(serializers.ModelSerializer):
    # school_year = SchoolYearSerializer(read_only=True)

    class Meta:
        model = LearningOutcomes
        fields = ['id', 'student', 'school_year',
                  'st_semester_conduct', 'nd_semester_conduct', ]
        # read_only_fields = ['school_year']

    def create(self, validated_data):
        return LearningOutcomes.objects.create(
            student=validated_data['student'],
            school_year=validated_data['school_year'],
            st_semester_conduct=validated_data['st_semester_conduct'],
            nd_semester_conduct=validated_data['nd_semester_conduct'],
        )

# lay thong tin hanh kiem cua hoc sinh


class ConductStudentSerializer(serializers.ModelSerializer):
    school_year = SchoolYearSerializer()

    class Meta:
        model = LearningOutcomes
        fields = ['id', 'school_year',
                  'st_semester_conduct', 'nd_semester_conduct', ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_name']


class LectureSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    classes = ClassesSerializer()
    school_year = SchoolYearSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Lecture
        fields = ['id', 'teacher', 'subject',
                  'classes', 'school_year', 'st_due_input', 'nd_due_input', ]


class MarksRegularySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarksRegulary
        fields = ['id', 'marks_ref', 'semester', 'input_date',
                  'point', 'note']
        read_only_fields = ['id', ]


class MarksSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    lecture = LectureSerializer(read_only=True)
    marksregulary = MarksRegularySerializer(read_only=True, many=True)

    class Meta:
        model = Marks
        fields = ['id', 'student', 'lecture',
                  'mid_st_semester_point', 'end_st_semester_point',
                  'mid_nd_semester_point', 'end_nd_semester_point',
                  'is_public', 'is_locked', 'marksregulary']
        read_only_fields = ['is_public', 'is_locked']
        # extra_kwargs = {'student': {'required': False},
        #                 'lecture': {'required': False}}


# Toan bo diem cua 1 hoc sinh
class MarksRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarksRegulary
        fields = ['id', 'marks_ref', 'semester', 'point']
        read_only_fields = ['id', ]


class LectureForStudentSerializer(serializers.ModelSerializer):
    school_year = SchoolYearSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Lecture
        fields = ['id', 'subject',
                  'classes', 'school_year']
        read_only_fields = ['id', ]


class MarksSerializerStudent(serializers.ModelSerializer):
    marksregulary = MarksRegSerializer(read_only=True, many=True)
    lecture = LectureForStudentSerializer(read_only=True)

    class Meta:
        model = Marks
        fields = ['id', 'lecture',
                  'mid_st_semester_point', 'end_st_semester_point',
                  'mid_nd_semester_point', 'end_nd_semester_point',
                  'marksregulary']
        # read_only_fields = ['is_public', 'is_locked']

# TOAN BO DIEM CUA MOT MON HOC, 1 LOP


class StudentSerializerForMarks(serializers.ModelSerializer):
    user = UserSerializerForMarks(read_only=True)
    # classes = ClassesSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['user', ]


class MarksSerializerClasses(serializers.ModelSerializer):
    marksregulary = MarksRegSerializer(read_only=True, many=True)
    student = StudentSerializerForMarks(read_only=True)

    class Meta:
        model = Marks
        fields = ['id', 'student',
                  'mid_st_semester_point', 'end_st_semester_point',
                  'mid_nd_semester_point', 'end_nd_semester_point',
                  'marksregulary']


# # TOAN BO DIEM CUA 1 lop hoc, tât ca cac mon
# class StudentSerializerForMarks(serializers.ModelSerializer):
#     user = UserSerializerForMarks(read_only=True)
#     # classes = ClassesSerializer(read_only=True)

#     class Meta:
#         model = Student
#         fields = ['user', ]
class LectureAdminClassSerializer(serializers.ModelSerializer):
    # school_year = SchoolYearSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Lecture
        fields = ['id', 'subject']
        read_only_fields = ['id', ]


class MarksSerializerAdminClass(serializers.ModelSerializer):
    marksregulary = MarksRegSerializer(read_only=True, many=True)
    student = StudentSerializerForMarks(read_only=True)
    lecture = LectureAdminClassSerializer(read_only=True)

    class Meta:
        model = Marks
        fields = ['id', 'student', 'lecture',
                  'mid_st_semester_point', 'end_st_semester_point',
                  'mid_nd_semester_point', 'end_nd_semester_point',
                  'marksregulary']

# Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'post_date']
        read_only_fields = ['id', ]


# Danh gia hanh kiem
class ConductSerializer(serializers.ModelSerializer):
    # student = StudentSerializerForMarks(read_only=True)
    user = UserSerializer(read_only=True)
    learningoutcomes = ConductStudentSerializer(many=True)

    class Meta:
        model = Student
        fields = ['user', 'learningoutcomes']
        # read_only_fields = ['id']
