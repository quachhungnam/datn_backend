from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from appmarks.views import (
    DepartmentView, DepartmentDetail, TeacherView, TeacherDetail, SubjectView, SubjectDetail,
    ClassesView, ClassesDetail, SchoolYearView, SchoolYearDetail, StudentView, StudentDetail,
    AcademicRecordView, AcademicRecordDetail, LectureView, LectureDetail,
    MarksView, MarksDetail, MarksRegularyView, MarksRegularyDetail,
    ActivitiesClassView,
    ActivitiesClassDetail,

    LectureList,
    # StudentsOfClass,
    # MarksOfClass,
    StudentsOfClass2,

    AddStudent,
    ImportData
)
app_name = 'appmarks'
urlpatterns = [
    path('import-data/', ImportData.as_view(), name='uploaddata'),
    path('uploadfile/', AddStudent.as_view(), name="upload"),

    path('departments/', DepartmentView.as_view()),
    path('departments/<int:pk>/', DepartmentDetail.as_view(),
         name='department-detail'),

    path('teachers/', TeacherView.as_view()),
    path('teachers/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),

    path('subjects/', SubjectView.as_view()),
    path('subjects/<int:pk>/', SubjectDetail.as_view(), name='subject-detail'),

    path('classes/', ClassesView.as_view()),
    path('classes/<int:pk>/', ClassesDetail.as_view(), name='classes-detail'),

    path('schoolyears/', SchoolYearView.as_view()),
    path('schoolyears/<int:pk>/', SchoolYearDetail.as_view(),
         name='schoolyear-detail'),

    path('students/', StudentView.as_view()),
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'),
    path('students/lectures/', StudentsOfClass2.as_view(), name='student-detail2'),

    path('AcademicRecord/', AcademicRecordView.as_view()),
    path('AcademicRecord/<int:pk>/', AcademicRecordDetail.as_view(),
         name='conduct-detail'),
    # path('AcademicRecord/classes/<int:class_id>/',
    #      StudentsOfClass.as_view(), name='student-class'),

    path('lectures/', LectureView.as_view()),
    path('lectures/<int:pk>/', LectureDetail.as_view(), name='lecture-detail'),
    # nam hoc nao giao vien nao day nhung gi
    # path('lectures/<int:teacher>/<int:schoolyear>/', LectureList.as_view()),

    path('marks/', MarksView.as_view(), name='list-marks'),
    path('marks/<int:pk>/', MarksDetail.as_view(), name='marks-detail'),
    # path('marks/lecture/<int:lecture_id>/',
    #      MarksOfClass.as_view(), name='marks-lecture'),

    path('marksregularys/', MarksRegularyView.as_view()),
    path('marksregularys/<int:pk>/', MarksRegularyDetail.as_view(),
         name='marksregulary-detail'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
