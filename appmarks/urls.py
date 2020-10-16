from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from appmarks.views import (
    DepartmentView, DepartmentDetail, TeacherView, TeacherDetail, SubjectView, SubjectDetail,
    ClassesView, ClassesDetail, SchoolYearView, SchoolYearDetail, StudentView, StudentDetail,
    ConductView, ConductDetail, LectureView, LectureDetail,
    MarksView, MarksDetail, MarksRegularyView, MarksRegularyDetail
)

urlpatterns = [
    path('departments/', DepartmentView.as_view()),
    path('departments/<int:pk>/', DepartmentDetail.as_view()),

    path('teachers/', TeacherView.as_view()),
    path('teachers/<int:pk>/', TeacherDetail.as_view()),

    path('subjects/', SubjectView.as_view()),
    path('subjects/<int:pk>/', SubjectDetail.as_view()),

    path('classes/', ClassesView.as_view()),
    path('classes/<int:pk>/', ClassesDetail.as_view()),

    path('schoolyears/', SchoolYearView.as_view()),
    path('schoolyears/<int:pk>/', SchoolYearDetail.as_view()),

    path('students/', StudentView.as_view()),
    path('students/<int:pk>/', StudentDetail.as_view()),

    path('conducts/', ConductView.as_view()),
    path('conducts/<int:pk>/', ConductDetail.as_view()),

    path('lectures/', LectureView.as_view()),
    path('lectures/<int:pk>/', LectureDetail.as_view()),

    path('marks/', MarksView.as_view()),
    path('marks/<int:pk>/', MarksDetail.as_view()),

    path('marksregularys/', MarksRegularyView.as_view()),
    path('marksregularys/<int:pk>/', MarksRegularyDetail.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
