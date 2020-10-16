from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from appmarks.views import (
    DepartmentView, DepartmentDetail, TeacherView, SubjectView, SubjectDetail)

urlpatterns = [
    path('departments/', DepartmentView.as_view()),
    path('departments/<int:pk>/', DepartmentDetail.as_view()),

    path('subjects/', SubjectView.as_view()),
    # path('classes/', ClassesView.as_view()),
    path('teachers/', TeacherView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
