from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from appmarks.models import (
    Department, Teacher, SchoolYear, Classes,
    Student, Conduct, Subject, Lecture, Marks, MarksRegulary)
from appmarks.serializiers import (
    DepartmentSerializer, TeacherSerializer, SchoolYearSerializer,
    StudentSerializer, ConductSerializer, SubjectSerializer,
    ClassesSerializer, LectureSerializer, MarksSerializer, MarksRegularySerializer)
from django.http import Http404

"""Department"""


class DepartmentView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


"""Teacher"""


class TeacherView(ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetail(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


"""Schoolyear"""


class SchoolYearView(ListCreateAPIView):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer


class SchoolYearDetail(RetrieveUpdateDestroyAPIView):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer


"""Classes"""


class ClassesView(ListCreateAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer


class ClassesDetail(RetrieveUpdateDestroyAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer


"""Student"""


class StudentView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


"""Conduct"""


class ConductView(ListCreateAPIView):
    queryset = Conduct.objects.all()
    serializer_class = ConductSerializer


class ConductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Conduct.objects.all()
    serializer_class = ConductSerializer


"""Department"""


class SubjectView(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetail(RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


"""Lecture"""


class LectureView(ListCreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class LectureDetail(RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class LectureList(ListAPIView):
    serializer_class = LectureSerializer

    def get_queryset(self):
        # teacher = self.request.user
        teacher = self.kwargs['teacher']
        schoolyear = self.kwargs['schoolyear']
        return Lecture.objects.filter(teacher__user__id=teacher, classes__school_year__id=schoolyear)


"""Marks"""


class MarksView(ListCreateAPIView):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer


class MarksDetail(RetrieveUpdateDestroyAPIView):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer


"""MarksRegulary"""


class MarksRegularyView(ListCreateAPIView):
    queryset = MarksRegulary.objects.all()
    serializer_class = MarksRegularySerializer


class MarksRegularyDetail(RetrieveUpdateDestroyAPIView):
    queryset = MarksRegulary.objects.all()
    serializer_class = MarksRegularySerializer
