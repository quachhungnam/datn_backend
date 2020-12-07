from django import forms
from django.shortcuts import redirect
from rest_framework import generics
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from appaccount.models import User
from appmarks.models import (
    Department, Teacher, SchoolYear, Classes,
    Student, LearningOutcomes, Subject, Lecture,
    Marks, MarksRegulary, AdminClass, Notice)
from appmarks.serializiers import (
    DepartmentSerializer, TeacherSerializer, SchoolYearSerializer,
    StudentSerializer, LearningOutcomesSerializer, AdminClassSerializer, SubjectSerializer,
    ClassesSerializer, LectureSerializer, MarksSerializer, MarksRegularySerializer,
    MarksSerializerStudent, MarksSerializerClasses, NoticeSerializer,MarksSerializerAdminClass)
from appaccount.serializiers import(UserSerializer)
from django.http import Http404
import pandas as pd
from pandas import ExcelFile
from datetime import datetime, date

# Create your views here.

"""
Department
"""


class DepartmentView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request, format=None):
        departments = Department.objects.all().order_by('department_name')
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
    permission_classes = (IsAuthenticated, IsAdminUser,)

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

    def patch(self, request, pk, format=None):
        department = self.get_object(pk)
        serializier = DepartmentSerializer(department, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""Teacher"""


class TeacherView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request, format=None):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(
            teachers, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        teacher = self.get_object(pk)
        serializier = TeacherSerializer(teacher, context={'request': request})
        return Response(serializier.data)

    def patch(self, request, pk, format=None):
        teacher = self.get_object(pk)
        user_data = request.data.get('user', None)
        if user_data is not None:
            if user_data.get('password') is not None:
                del user_data['password']
            serializier_user = UserSerializer(
                teacher.user, data=user_data, partial=True)
            if serializier_user.is_valid():
                serializier_user.save()
            del request.data['user']

        serializier = TeacherSerializer(
            teacher, data=request.data, partial=True)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        teacher = self.get_object(pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseList(generics.ListAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):

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
        classess = Classes.objects.all().order_by('class_name')
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

    def patch(self, request, pk, format=None):
        classes = self.get_object(pk)
        serializier = ClassesSerializer(classes, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        classes = self.get_object(pk)
        classes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializier = StudentSerializer(student, context={'request': request})
        return Response(serializier.data)

    def patch(self, request, pk, format=None):
        student = self.get_object(pk)
        user_data = request.data.get('user', None)
        if user_data is not None:
            if user_data.get('password') is not None:
                del user_data['password']
            serializier_user = UserSerializer(
                student.user, data=user_data, partial=True)
            if serializier_user.is_valid():
                serializier_user.save()
            del request.data['user']

        student = self.get_object(pk)
        serializier = StudentSerializer(
            student, data=request.data, partial=True)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentsOfClass(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        classes = self.kwargs['class_id']
        school_year = self.kwargs['school_year_id']
        # schoolyear = self.kwargs['schoolyear']
        return Student.objects.filter(marks_student__lecture__classes=classes, marks_student__lecture__school_year=school_year).distinct()


class StudentsOfLecture(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        lecture = self.kwargs['lecture_id']
        # school_year= self.kwargs['school_year_id']
        # schoolyear = self.kwargs['schoolyear']
        return Student.objects.filter(marks_student__lecture=lecture)


"""AdminClass"""


class AdminClassView(APIView):

    def get(self, request, format=None):
        adminclass = AdminClass.objects.all()
        serializer = AdminClassSerializer(
            adminclass, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AdminClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminClassDetail(APIView):
    def get_object(self, pk):
        try:
            return AdminClass.objects.get(pk=pk)
        except AdminClass.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        adminclass = self.get_object(pk)
        serializier = AdminClassSerializer(
            adminclass, context={'request': request})
        return Response(serializier.data)

    def patch(self, request, pk, format=None):
        adminclass = self.get_object(pk)
        serializier = AdminClassSerializer(
            adminclass, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        adminclass = self.get_object(pk)
        adminclass.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class AdminClassTeacher(generics.ListAPIView):
    serializer_class = AdminClassSerializer

    def get_queryset(self):
        teacher = self.kwargs['teacher_id']
        schoolyear = self.kwargs['schoolyear_id']
        return AdminClass.objects.filter(admin_teacher__user__id=teacher, school_year__id=schoolyear)


"""Conduct"""


class LearningOutcomesView(APIView):

    def get(self, request, format=None):
        learningoutcome = LearningOutcomes.objects.all()
        serializer = LearningOutcomesSerializer(
            learningoutcome, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LearningOutcomesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningOutcomesDetail(APIView):
    def get_object(self, pk):
        try:
            return LearningOutcomes.objects.get(pk=pk)
        except LearningOutcomes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        acamedicrecord = self.get_object(pk)
        serializier = LearningOutcomesSerializer(acamedicrecord)
        return Response(serializier.data)

    def patch(self, request, pk, format=None):
        LearningOutcomes = self.get_object(pk)
        serializier = LearningOutcomesSerializer(
            LearningOutcomes, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        LearningOutcomes = self.get_object(pk)
        LearningOutcomes.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class StudentRecord(generics.ListAPIView):
    serializer_class = LearningOutcomesSerializer

    def get_queryset(self):
        # teacher = self.request.user
        # teacher = self.kwargs['teacher']
        # schoolyear = self.kwargs['schoolyear']
        studentId = self.kwargs['studentId']
        return LearningOutcomes.objects.filter(student=studentId).order_by('-school_year')

# class StudentsOfClass(generics.ListAPIView):  # lay danh sach hoc sinh cua 1 lop
#     serializer_class = ConductSerializer

#     def get_queryset(self):
#         class_id = self.kwargs['class_id']
#         # schoolyear = self.kwargs['schoolyear']
#         return Conduct.objects.filter(classes__id=class_id)


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

    def patch(self, request, pk, format=None):
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

    def patch(self, request, pk, format=None):
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
        # print(teacher)
        # print(schoolyear)
        return Lecture.objects.filter(teacher__user__id=teacher, school_year__id=schoolyear)


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

    def patch(self, request, pk, format=None):
        marks = self.get_object(pk)
        # print(request.data)
        for key in list(request.data.keys()):  # Use a list instead of a view
            if request.data[key] == '':
                request.data[key] = None  # Delete a key from prices

        serializier = MarksSerializer(marks, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        # print(serializier.errors)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        marks = self.get_object(pk)
        marks.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


# toan bo diem cua 1 hoc sinh trong 3 nam hoc
class MarkStudent(generics.ListAPIView):
    serializer_class = MarksSerializerStudent

    def get_queryset(self):
        studentId = self.kwargs['studentId']
        return Marks.objects.filter(student=studentId).order_by('lecture')


# class MarksOfClass(generics.ListAPIView):
#     serializer_class = MarksSerializer

#     def get_queryset(self):
#         studentId = self.kwargs['studentId']
#         lecture_id = self.kwargs['lecture_id']
#         return Marks.objects.filter(student=studentId,  lecture__id=lecture_id)


# diem cua 1 hoc sinh trong 1 nam hoc
class MarksByYear(generics.ListAPIView):
    serializer_class = MarksSerializerAdminClass

    def get_queryset(self):
        studentId = self.kwargs['studentId']
        school_year = self.kwargs['school_year']
        return Marks.objects.filter(student=studentId,  lecture__school_year=school_year)


# diem 1 mon hoc cua 1 lop hoc
class MarksOfLecture(generics.ListAPIView):
    serializer_class = MarksSerializerClasses

    def get_queryset(self):
        lecture_id = self.kwargs['lecture_id']
        return Marks.objects.filter(lecture__id=lecture_id).order_by('student__user__first_name')


# toan bo diem cua 1 lop' hoc trong 1 nam hoc
class MarksOfClass(generics.ListAPIView):
    serializer_class = MarksSerializerAdminClass

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        year_id = self.kwargs['year_id']
        return Marks.objects.filter(lecture__classes=class_id, lecture__school_year=year_id).order_by('student', 'lecture')


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

    def patch(self, request, pk, format=None):
        marksregulary = self.get_object(pk)
        for key in list(request.data.keys()):
            if request.data[key] == '':
                request.data[key] = None
        serializier = MarksRegularySerializer(marksregulary, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        # print(serializier.errors)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        marksregulary = self.get_object(pk)
        marksregulary.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


"""Notice"""


class NoticeView(APIView):

    def get(self, request, format=None):
        notices = Notice.objects.all().order_by('-post_date', 'title')
        serializer = NoticeSerializer(
            notices, many=True, context={'request': request})
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = NoticeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticeDetail(APIView):
    def get_object(self, pk):
        try:
            return Notice.objects.get(pk=pk)
        except Notice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        marksregulary = self.get_object(pk)
        serializier = NoticeSerializer(marksregulary)
        return Response(serializier.data)

    # def patch(self, request, pk, format=None):
    #     marksregulary = self.get_object(pk)
    #     for key in list(request.data.keys()):
    #         if request.data[key] == '':
    #             request.data[key] = None
    #     serializier = NoticeSerializer(marksregulary, data=request.data)
    #     if serializier.is_valid():
    #         serializier.save()
    #         return Response(serializier.data)
    #     # print(serializier.errors)
    #     return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     marksregulary = self.get_object(pk)
    #     marksregulary.delete()
    #     return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


"""Teacher"""


class AddStudent(APIView):
    #  @method_decorator(login_required)
    # luu tat ca du lieu vao co so du lieu
    parser_class = (MultiPartParser,)

    def post(self, request, format=None):
        # print(request.data)
        try:
            # print(request.data['fileanh'])
            # print(request.data)

            f = request.data.getlist("fileanh")
            # print(f)
            df = pd.read_excel(
                request.FILES['fileanh'], sheet_name=0, index_col=0)
            # xong roi luu vao DB
            # print(df)

            return Response({"success": 'success'}, status=status.HTTP_201_CREATED)

        except:
            return Response({"success": 'fail'}, status=status.HTTP_201_CREATED)


class UploadFileForm(forms.Form):
    data_student = forms.FileField()


class ImportData(APIView):
    parser_class = (MultiPartParser,)
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        if not request.user.is_superuser:
            return render(
                request, "admin/login.html"
            )
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_data_student = request.FILES["data_student"]
            df = pd.read_excel(file_data_student,
                               sheet_name=0, index_col=0)
            for row in df.itertuples():
                try:
                    current_year = date.today().year
                    classes = Classes.objects.filter(
                        course_year=current_year, class_name__iexact=row[4]).first()
                    if classes is None:
                        classes = Classes(
                            class_name=row[4]
                        )
                    classes.save()
                    # them hoc sinh
                    full_name = row[2].split(' ', 1)
                    full_birthday = row[3]

                    Student.objects.create(
                        username=row[1],
                        password=str(row[1]),
                        last_name=full_name[0],  # ho
                        first_name=full_name[1],  # ten dem va ten
                        course_year=current_year,
                        birthday=full_birthday,
                        classes=classes,
                    )
                    print('success')
                except:
                    print('fail create')
                    # print('error')
                    pass

        # print(reader)
        # Create Hero objects from passed in data
        # ...
        # self.message_user(request, "Your csv file has been imported")
        return redirect("..")

    def get(self, request, fortmat=None):
        if not request.user.is_superuser:
            return render(
                request, "admin/login.html"
            )
        form = UploadFileForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )
