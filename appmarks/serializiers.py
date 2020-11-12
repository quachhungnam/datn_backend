from rest_framework import serializers
from appmarks.models import (Department, Teacher, SchoolYear, Classes, Student,
                             Subject, Lecture, Marks, MarksRegulary, ActivitiesClass, AcademicRecord)
from appaccount.serializiers import UserSerializer
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
        fields = ['id', 'from_year', 'to_year', 'status']
        read_only_fields = ['id']


class ClassesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classes
        fields = ['id', 'class_name', 'course_year', 'student']
        read_only_fields = ['id']


class ActivitiesClassSerializer(serializers.ModelSerializer):
    classes= ClassesSerializer()
    school_year=SchoolYearSerializer()
    class Meta:
        model = ActivitiesClass
        fields = ['id', 'classes', 'form_teacher', 'school_year']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'is_crew', 'classes']

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
            is_crew=validated_data.get('is_crew', False),
        )


class AcamedicRecordSerializer(serializers.ModelSerializer):
    school_year = SchoolYearSerializer()

    class Meta:
        model = AcademicRecord
        fields = ['id', 'student', "school_year",
                  "gpa_first_semester", "gpa_second_semester", "gpa_year",
                  "conduct_stsemester", "conduct_ndsemester", "conduct_gpasemester",
                  "rating", "rating_stsemester", "rating_ndsemester"
                  ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'grades', 'descriptions']


class LectureSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    classes = ClassesSerializer()
    school_year = SchoolYearSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Lecture
        fields = ['id', 'teacher', 'subject',
                  'classes', 'school_year', 'status']


class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = ['id', 'student', 'lecture',
                  'semester', 'mid_semester_point', 'gpa_semester_point',
                  'gpa_year_point', 'is_public', 'is_locked', 'due_input']


class MarksRegularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = ['id', "student", "lecture", "semester", "test_date",
                  "point", "note", "is_public", "is_locked", 'times']
        read_only_fields = ['id']
