from rest_framework import serializers
from appmarks.models import Department, Teacher, SchoolYear, Classes, Student, Conduct, Subject, Lecture, Marks, MarksRegulary
from appaccount.serializiers import UserSerializer


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'introduction']
        # fields = '__all__'


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False,)
    department = DepartmentSerializer()

    class Meta:
        model = Teacher
        exclude = ['url']


class SchoolYearSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SchoolYear
        # fields = '__all__'
        exclude = ['url']


class ClassesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classes
        exclude = ['url']


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        exclude = ['url']
        # fields = '__all__'


class ConductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conduct
        # fields = '__all__'
        exclude = ['url']


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        # fields = '__all__'
        exclude = ['url']


class LectureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecture
        # fields = '__all__'
        exclude = ['url']


class MarksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Marks
        # fields = '__all__'
        exclude = ['url']


class MarksRegularySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarksRegulary
        # fields = '__all__'
        exclude = ['url']
