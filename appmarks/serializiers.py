from rest_framework.serializers import (HyperlinkedRelatedField, HyperlinkedModelSerializer,
                                        StringRelatedField, ModelSerializer, PrimaryKeyRelatedField)
from appmarks.models import (Department, Teacher, SchoolYear, Classes, Student,
                             Subject, Lecture, Marks, MarksRegulary, ActivitiesClass, AcademicRecord)
from appaccount.serializiers import UserSerializer


class DepartmentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'introduction']
        read_only_fields = ['id']


class TeacherSerializer(HyperlinkedModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'department']
        read_only_fields = ['user']


class SchoolYearSerializer(HyperlinkedModelSerializer):
    # classes=PrimaryKeyRelatedField(many=True,read_only=True)
    # classes = serializer_related_field
    class Meta:
        model = SchoolYear
        fields = ['id', 'from_year', 'to_year', 'status']
        read_only_fields = ['id']


class ClassesSerializer(HyperlinkedModelSerializer):
    # school_year = SchoolYearSerializer()
    # form_teacher = TeacherSerializer()

    class Meta:
        model = Classes
        fields = ['id', 'school_year', 'class_name', 'course_year']
        read_only_fields = ['id']


class ActivitiesClassSerializer(HyperlinkedModelSerializer):
    # user = UserSerializer(many=False)

    class Meta:
        model = ActivitiesClass
        fields = ['id', 'classes', 'form_teacher', 'school_year']


class StudentSerializer(HyperlinkedModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = ['user', 'is_crew', 'classes']


class AcamedicRecordSerializer(HyperlinkedModelSerializer):
    # student = StudentSerializer()
    # classes = ClassesSerializer()

    class Meta:
        model = AcademicRecord
        fields = ['id', 'student', "school_year",
                  "gpa_first_semester", "gpa_second_semester", "gpa_year",
                  "conduct_stsemester", "conduct_ndsemester", "conduct_gpasemester", "rating"
                  ]


class SubjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'student', 'school_year', 'gpa_first_semester',
                  'gpa_second_semester', 'gpa_year', 'conduct_stsemester',
                  'conduct_ndsemester', 'conduct_gpasemester', 'rating_year']


class LectureSerializer(HyperlinkedModelSerializer):
    # teacher = TeacherSerializer()
    # subject = SubjectSerializer()
    # classes = ClassesSerializer()

    # marks =

    class Meta:
        model = Lecture
        fields = ['id', 'teacher', 'subject',
                  'classes', 'school_year', 'status']


class MarksSerializer(HyperlinkedModelSerializer):
    # marks_ref = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Marks
        fields = ['id', 'student', 'lecture',
                  'semester', 'mid_semester_point', 'gpa_semester_point',
                  'gpa_year_point', 'is_public', 'is_locked', 'due_input']
        # fields = '__all__'
        # exclude=['url']


class MarksRegularySerializer(HyperlinkedModelSerializer):
    # lecture = LectureSerializer(read_only=True)
    # student = StudentSerializer(read_only=True)
    # marks_regulary = MarksRegularySerializer(many=True, read_only=True)

    class Meta:
        model = Marks
        fields = ['id', "student", "lecture", "semester", "test_date",
                  "point", "note", "is_public", "is_locked", 'times']
        read_only_fields = ['id']
        # extra_kwargs = {
        #     'lecture': {'required': False},
        #     'student': {'required': False},
        #     'marks_regulary': {'required': False},

        # }

        # exclude = ['url']
