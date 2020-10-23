from rest_framework.serializers import (HyperlinkedRelatedField, HyperlinkedModelSerializer,
                                        StringRelatedField, ModelSerializer, PrimaryKeyRelatedField)
from appmarks.models import (Department, Teacher, SchoolYear, Classes, Student,
                             Conduct, Subject, Lecture, Marks, MarksRegulary)
from appaccount.serializiers import UserSerializer


class DepartmentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'introduction']


class TeacherSerializer(HyperlinkedModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'department']


class SchoolYearSerializer(HyperlinkedModelSerializer):
    # classes=PrimaryKeyRelatedField(many=True,read_only=True)
    # classes = serializer_related_field
    class Meta:
        model = SchoolYear
        fields = ['id', 'from_year', 'to_year', ]


class ClassesSerializer(HyperlinkedModelSerializer):
    school_year = SchoolYearSerializer()
    form_teacher = TeacherSerializer()

    class Meta:
        model = Classes
        fields = ['id', 'school_year', 'form_teacher', 'class_name']


class StudentSerializer(HyperlinkedModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = ['user', 'is_crew']


class ConductSerializer(HyperlinkedModelSerializer):
    student = StudentSerializer()
    classes = ClassesSerializer()

    class Meta:
        model = Conduct
        fields = ['id', 'student', "conduct_stsemester",
                  "conduct_ndsemester", "conduct_gpasemester", "classes"]


class SubjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'level', 'descriptions']


class LectureSerializer(HyperlinkedModelSerializer):
    teacher = TeacherSerializer()
    subject = SubjectSerializer()
    classes = ClassesSerializer()

    # marks =

    class Meta:
        model = Lecture
        fields = ['id', 'teacher', 'subject', 'classes']


class MarksSerializer(HyperlinkedModelSerializer):
    lecture = LectureSerializer()
    student = StudentSerializer()

    class Meta:
        model = Marks
        fields = ['id',
                  "mid_first_semester",
                  "end_first_semester",
                  "gpa_first_semester",
                  "mid_second_semester",
                  "end_second_semester",
                  "gpa_second_semester",
                  "gpa_year",
                  "is_public",
                  "is_locked",
                  "student",
                  "lecture"]


class MarksRegularySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MarksRegulary
        exclude = ['url']
