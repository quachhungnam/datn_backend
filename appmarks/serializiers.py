from rest_framework.serializers import HyperlinkedModelSerializer
from appmarks.models import Department, Teacher, SchoolYear, Classes, Student, Conduct, Subject, Lecture, Marks, MarksRegulary
from appaccount.serializiers import UserSerializer


class DepartmentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'introduction']
        # fields = '__all__'


class TeacherSerializer(HyperlinkedModelSerializer):
    user = UserSerializer(many=False,)
    department = DepartmentSerializer()

    class Meta:
        model = Teacher
        exclude = ['url']


class SchoolYearSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SchoolYear
        # fields = '__all__'
        exclude = ['url']


class ClassesSerializer(HyperlinkedModelSerializer):
    school_year = SchoolYearSerializer()
    form_teacher = TeacherSerializer()

    class Meta:
        model = Classes
        exclude = ['url']


class StudentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Student
        exclude = ['url']
        # fields = '__all__'


class ConductSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Conduct
        # fields = '__all__'
        exclude = ['url']


class SubjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        # fields = '__all__'
        exclude = ['url']


class LectureSerializer(HyperlinkedModelSerializer):
    teacher = TeacherSerializer()
    subject = SubjectSerializer()
    classes = ClassesSerializer()

    class Meta:
        model = Lecture
        # fields = '__all__'
        exclude = ['url']


class MarksSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Marks
        # fields = '__all__'
        exclude = ['url']


class MarksRegularySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MarksRegulary
        # fields = '__all__'
        exclude = ['url']
