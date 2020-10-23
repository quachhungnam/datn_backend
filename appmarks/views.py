from rest_framework import generics
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
# Create your views here.


# class HelloView(APIView):
#     # permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)

# Lay thong tin ca nhan
# Lay tat ca diem cua hoc sinh theo nam


"""
Department
"""


class DepartmentView(APIView):

    def get(self, request, format=None):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(
            departments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        department = self.get_object(pk)
        serializier = DepartmentSerializer(
            department, context={'request': request})
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        department = self.get_object(pk)

        serializier = DepartmentSerializer(department, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        department = self.get_object(pk)
        department.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


"""Teacher"""


class TeacherView(APIView):

    def get(self, request, format=None):
        teachers = Teacher.objects.all()
        print(teachers)
        serializer = TeacherSerializer(
            teachers, many=True, context={'request': request})
        return Response(serializer.data)


class TeacherDetail(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TeacherSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = TeacherSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseList(generics.ListAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """

        return Teacher.objects.filter(user_id=2)


"""
School Year
"""


class SchoolYearView(APIView):

    def get(self, request, format=None):
        schoolyears = SchoolYear.objects.all().order_by('-to_year', '-from_year')
        serializer = SchoolYearSerializer(
            schoolyears, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SchoolYearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolYearDetail(APIView):
    def get_object(self, pk):
        try:
            return SchoolYear.objects.get(pk=pk)
        except SchoolYear.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        schoolyear = self.get_object(pk)
        serializier = SchoolYearSerializer(schoolyear)
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        schoolyear = self.get_object(pk)
        serializier = SchoolYearSerializer(schoolyear, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schoolyear = self.get_object(pk)
        schoolyear.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


"""Class"""


class ClassesView(APIView):

    def get(self, request, format=None):
        classess = Classes.objects.all()
        serializer = ClassesSerializer(
            classess, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClassesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassesDetail(APIView):
    def get_object(self, pk):
        try:
            return Classes.objects.get(pk=pk)
        except Classes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        classes = self.get_object(pk)
        serializier = ClassesSerializer(classes)
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        classes = self.get_object(pk)
        serializier = ClassesSerializer(classes, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        classes = self.get_object(pk)
        classes.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


"""Student"""


class StudentView(APIView):

    def get(self, request, format=None):
        students = Student.objects.all()
        serializer = StudentSerializer(
            students, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializier = StudentSerializer(student, context={'request': request})
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        student = self.get_object(pk)
        serializier = StudentSerializer(student, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        student.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


"""Conduct"""


class ConductView(APIView):

    def get(self, request, format=None):
        conducts = Conduct.objects.all()
        serializer = ConductSerializer(
            conducts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConductDetail(APIView):
    def get_object(self, pk):
        try:
            return Conduct.objects.get(pk=pk)
        except Conduct.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conduct = self.get_object(pk)
        serializier = ConductSerializer(conduct)
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        conduct = self.get_object(pk)
        serializier = ConductSerializer(conduct, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        conduct = self.get_object(pk)
        conduct.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class StudentsOfClass(generics.ListAPIView):  # lay danh sach hoc sinh cua 1 lop
    serializer_class = ConductSerializer

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        # schoolyear = self.kwargs['schoolyear']
        return Conduct.objects.filter(classes__id=class_id)


class StudentsOfClass2(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        # class_id = self.kwargs['class_id']
        # schoolyear = self.kwargs['schoolyear']
        return Student.objects.filter(conduct__classes__lecture__id=2)


"""Subject"""


class SubjectView(APIView):

    def get(self, request, format=None):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(
            subjects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectDetail(APIView):
    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        subject = self.get_object(pk)
        serializier = SubjectSerializer(subject)
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        subject = self.get_object(pk)
        serializier = SubjectSerializer(subject, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        subject = self.get_object(pk)
        subject.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


""""Lecture"""


class LectureView(APIView):

    def get(self, request, format=None):
        lectures = Lecture.objects.all()
        serializer = LectureSerializer(
            lectures, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureDetail(APIView):
    def get_object(self, pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        lecture = self.get_object(pk)
        serializier = LectureSerializer(lecture, context={'request': request})
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        lecture = self.get_object(pk)
        serializier = LectureSerializer(lecture, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        lecture = self.get_object(pk)
        lecture.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class LectureList(generics.ListAPIView):
    serializer_class = LectureSerializer

    def get_queryset(self):
        # teacher = self.request.user
        teacher = self.kwargs['teacher']
        schoolyear = self.kwargs['schoolyear']
        return Lecture.objects.filter(teacher__user__id=teacher, classes__school_year__id=schoolyear)


"""Marks"""


class MarksView(APIView):

    def get(self, request, format=None):
        markss = Marks.objects.all()
        serializer = MarksSerializer(
            markss, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MarksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarksDetail(APIView):
    def get_object(self, pk):
        try:
            return Marks.objects.get(pk=pk)
        except Marks.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        marks = self.get_object(pk)
        serializier = MarksSerializer(marks, context={'request': request})
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        marks = self.get_object(pk)
        serializier = MarksSerializer(marks, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        marks = self.get_object(pk)
        marks.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class MarksOfClass(generics.ListAPIView):
    serializer_class = MarksSerializer
    # serializer_class = LectureSerializer

    def get_queryset(self):
        # teacher = self.request.user
        # teacher = self.kwargs['teacher']
        # schoolyear = self.kwargs['schoolyear']
        return Marks.objects.filter(lecture__id=1)


"""Diem DGTX"""


class MarksRegularyView(APIView):

    def get(self, request, format=None):
        marksregularys = MarksRegulary.objects.all()
        serializer = MarksRegularySerializer(
            marksregularys, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MarksRegularySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarksRegularyDetail(APIView):
    def get_object(self, pk):
        try:
            return MarksRegulary.objects.get(pk=pk)
        except MarksRegulary.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        marksregulary = self.get_object(pk)
        serializier = MarksRegularySerializer(marksregulary)
        return Response(serializier.data)

    def put(self, request, pk, format=None):
        marksregulary = self.get_object(pk)
        serializier = MarksRegularySerializer(marksregulary, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        marksregulary = self.get_object(pk)
        marksregulary.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


"""Teacher"""


class TeacherView(APIView):

    def get(self, request, format=None):
        teachers = Teacher.objects.all().prefetch_related('department')
        print(teachers)
        serializer = TeacherSerializer(
            teachers, many=True, context={'request': request})
        return Response(serializer.data)


class TeacherDetail(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TeacherSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = TeacherSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # class ClassesView(APIView):

    #     def get(self, request, format=None):
    #         serializer_context = {
    #             'request': request,
    #         }
    #         departments = Classes.objects.all()
    #         serializer = ClassesSerializer(departments, context=serializer_context)
    #         # serializer = ClassesSerializer(
    #         #     departments, many=True,)

    #         return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = DepartmentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #   def getByUsername(self, request, username):
    #         serializer_context = {
    #             'request': request,
    #         }
    #         user = get_object_or_404(User, username=username)
    #         return Response(UserSerializer(user, context=serializer_context).data, status=status.HTTP_200_OK)
