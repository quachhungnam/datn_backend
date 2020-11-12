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
    Student, AcademicRecord, Subject, Lecture, Marks, MarksRegulary, ActivitiesClass)
from appmarks.serializiers import (
    DepartmentSerializer, TeacherSerializer, SchoolYearSerializer,
    StudentSerializer, AcamedicRecordSerializer, ActivitiesClassSerializer, SubjectSerializer,
    ClassesSerializer, LectureSerializer, MarksSerializer, MarksRegularySerializer)
from appaccount.serializiers import(UserSerializer)
from django.http import Http404
import pandas as pd
from pandas import ExcelFile

# Create your views here.

"""
Department
"""


class DepartmentView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

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


"""ActivitiesClass"""


class ActivitiesClassView(APIView):

    def get(self, request, format=None):
        activitiesclass = ActivitiesClass.objects.all()
        serializer = ActivitiesClassSerializer(
            activitiesclass, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ActivitiesClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivitiesClassDetail(APIView):
    def get_object(self, pk):
        try:
            return ActivitiesClass.objects.get(pk=pk)
        except ActivitiesClass.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        activitiesclass = self.get_object(pk)
        serializier = ActivitiesClassSerializer(
            activitiesclass, context={'request': request})
        return Response(serializier.data)

    def patch(self, request, pk, format=None):
        activitiesclass = self.get_object(pk)
        serializier = ActivitiesClassSerializer(
            activitiesclass, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        activitiesclass = self.get_object(pk)
        activitiesclass.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class ActivitiesClassTeacher(generics.ListAPIView):
    serializer_class = ActivitiesClassSerializer

    def get_queryset(self):
        teacher = self.kwargs['teacher_id']
        schoolyear = self.kwargs['schoolyear_id']
        return ActivitiesClass.objects.filter(form_teacher__user__id=teacher, school_year__id=schoolyear)


"""Conduct"""


class AcademicRecordView(APIView):

    def get(self, request, format=None):
        acamedicrecord = AcademicRecord.objects.all()
        serializer = AcamedicRecordSerializer(
            acamedicrecord, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AcademicRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcademicRecordDetail(APIView):
    def get_object(self, pk):
        try:
            return AcademicRecord.objects.get(pk=pk)
        except AcademicRecord.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        acamedicrecord = self.get_object(pk)
        serializier = AcamedicRecordSerializer(acamedicrecord)
        return Response(serializier.data)

    def patch(self, request, pk, format=None):
        academicrecord = self.get_object(pk)
        serializier = AcademicRecordSerializer(
            academicrecord, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academicrecord = self.get_object(pk)
        academicrecord.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class StudentRecord(generics.ListAPIView):
    serializer_class = AcamedicRecordSerializer

    def get_queryset(self):
        # teacher = self.request.user
        # teacher = self.kwargs['teacher']
        # schoolyear = self.kwargs['schoolyear']
        studentId = self.kwargs['studentId']
        return AcademicRecord.objects.filter(student=studentId)

# class StudentsOfClass(generics.ListAPIView):  # lay danh sach hoc sinh cua 1 lop
#     serializer_class = ConductSerializer

#     def get_queryset(self):
#         class_id = self.kwargs['class_id']
#         # schoolyear = self.kwargs['schoolyear']
#         return Conduct.objects.filter(classes__id=class_id)


class StudentsOfClass2(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        # class_id = self.kwargs['class_id']
        # schoolyear = self.kwargs['schoolyear']
        return Student.objects.filter(classes=1)


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
        print(teacher)
        print(schoolyear)
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
        serializier = MarksSerializer(marks, data=request.data)
        if serializier.is_valid():
            serializier.save()
            return Response(serializier.data)
        return Response(serializier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        marks = self.get_object(pk)
        marks.delete()
        return Response({"detail": "delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class MarkStudent(generics.ListAPIView):
    serializer_class = MarksSerializer

    def get_queryset(self):
        # teacher = self.request.user
        # teacher = self.kwargs['teacher']
        studentId = self.kwargs['studentId']
        school_year = self.kwargs['school_year']
        return Marks.objects.filter(student=studentId, lecture__school_year__id=school_year).order_by('lecture', 'semester')


class MarksOfClass(generics.ListAPIView):
    serializer_class = MarksSerializer

    def get_queryset(self):
        # teacher = self.request.user
        # teacher = self.kwargs['teacher']
        studentId = self.kwargs['studentId']
        lecture_id = self.kwargs['lecture_id']
        return Marks.objects.filter(student=studentId,  lecture__id=lecture_id)


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


class AddStudent(APIView):
    #  @method_decorator(login_required)
    # luu tat ca du lieu vao co so du lieu
    parser_class = (MultiPartParser,)

    def post(self, request, format=None):
        print(request.data)
        try:
            # print(request.data['fileanh'])
            # print(request.data)

            f = request.data.getlist("fileanh")
            # print(f)
            df = pd.read_excel(
                request.FILES['fileanh'], sheet_name=0, index_col=0)
            # xong roi luu vao DB
            print(df)

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
                classes = Classes.objects.filter(
                    course_year=row[4], class_name__iexact=row[5]).first()
                if classes is None:
                    classes = Classes(
                        class_name=row[5]
                    )
                    classes.save()
                print(classes)
                student = Student.objects.create(
                    username=row[0],
                    password=str(row[0]),
                    first_name=row[1],
                    last_name=row[2],
                    gender=row[3],
                    course_year=row[4],
                    # birthday=row[''],
                    # email=validated_data['user'].get('email', ''),
                    # phone_number=validated_data['user'].get(
                    #     'phone_number', ''),
                    # address=validated_data['user'].get('address', ''),
                    classes=classes,
                    # is_crew=validated_data.get('is_crew', False),
                )
                print('tao tai khoan thanh cong')

                # print(df.iloc[0])
                # print(df.iloc[0][0])

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
