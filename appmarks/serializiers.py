from rest_framework import serializers
from appmarks.models import (Department, Teacher, SchoolYear, Classes, Student,
                             Subject, Lecture, Marks, MarksRegulary, ActivitiesClass, AcademicRecord)
from appaccount.serializiers import UserSerializer
from appaccount.models import User
from django.db import models


class UserManager(models.Manager):
    def create(self, username, password, is_crew):
        user = User(username=username, password=password)
        user.save()
        student = Student(
            user=user,
            is_crew=is_crew,
        )
        student.save()
        return student


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'introduction']
        read_only_fields = ['id']


class TeacherSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Teacher
        fields = ['user', 'department']


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = ['id', 'from_year', 'to_year', 'status']
        read_only_fields = ['id']


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'class_name', 'course_year']
        read_only_fields = ['id']


class ActivitiesClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitiesClass
        fields = ['id', 'classes', 'form_teacher', 'school_year']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'is_crew', 'classes']

    def create(self, validated_data):
        user = User(
            username=validated_data['user']['username'],
        )
        user.set_password(validated_data['user']['password'])
        user.save()

        student = Student(
            user=user,
            classes=validated_data['classes']
        )
        student.save()
        return student

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        profile = instance.profile
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.is_premium_member = profile_data.get(
            'is_premium_member',
            profile.is_premium_member
        )
        profile.has_support_contract = profile_data.get(
            'has_support_contract',
            profile.has_support_contract
        )

        student.save()

        return student


class AcamedicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = ['id', 'student', "school_year",
                  "gpa_first_semester", "gpa_second_semester", "gpa_year",
                  "conduct_stsemester", "conduct_ndsemester", "conduct_gpasemester", "rating"
                  ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'student', 'school_year', 'gpa_first_semester',
                  'gpa_second_semester', 'gpa_year', 'conduct_stsemester',
                  'conduct_ndsemester', 'conduct_gpasemester', 'rating_year']


class LectureSerializer(serializers.ModelSerializer):
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
