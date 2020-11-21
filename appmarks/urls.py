from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from appmarks.views import (
    DepartmentView, DepartmentDetail, TeacherView, TeacherDetail, SubjectView, SubjectDetail,
    ClassesView, ClassesDetail, SchoolYearView, SchoolYearDetail, StudentView, StudentDetail,
    LearningOutcomesView, LearningOutcomesDetail, LectureView, LectureDetail,
    MarksView, MarksDetail, MarksRegularyView, MarksRegularyDetail,
    ActivitiesClassView,
    ActivitiesClassDetail,
    LectureList,
    # StudentsOfClass,
    StudentsOfClass,
    AddStudent,
    ImportData,
    StudentRecord,
    MarkStudent,
    ActivitiesClassView,
    ActivitiesClassDetail,
    ActivitiesClassTeacher,
    StudentsOfLecture,
    MarksOfLecture,
    MarksByYear,
    MarksOfClass
)
app_name = 'appmarks'
urlpatterns = [
    path('import-data/', ImportData.as_view(), name='uploaddata'),
    path('uploadfile/', AddStudent.as_view(), name="upload"),

    path('departments/', DepartmentView.as_view()),
    path('departments/<int:pk>/', DepartmentDetail.as_view(),
         name='department-detail'),

    path('activitiesclass/', ActivitiesClassView.as_view()),
    path('activitiesclass/<int:pk>/', ActivitiesClassDetail.as_view(),
         name='activitiesclass-detail'),
    path('activitiesclass/teacher/<int:teacher_id>/schoolyear/<int:schoolyear_id>/',
         ActivitiesClassTeacher.as_view(),),

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
    path('students/classes/<int:class_id>/schoolyear/<int:school_year_id>/',
         StudentsOfClass.as_view(), name='student-detail2'),
    path('students/lecture/<int:lecture_id>/',
         StudentsOfLecture.as_view(), name='student-detail3'),

    path('learningoutcome/', LearningOutcomesView.as_view()),
    path('learningoutcome/<int:pk>/', LearningOutcomesDetail.as_view(),
         name='conduct-detail'),
    path('learningoutcome/student/<int:studentId>/', StudentRecord.as_view()),

    # path('AcademicRecord/classes/<int:class_id>/',
    #      StudentsOfClass.as_view(), name='student-class'),

    path('lectures/', LectureView.as_view()),
    path('lectures/<int:pk>/', LectureDetail.as_view(), name='lecture-detail'),
    # nam hoc nao giao vien nao day nhung gi
    path('lectures/teacher/<int:teacher>/schoolyear/<int:schoolyear>/',
         LectureList.as_view()),

    path('marks/', MarksView.as_view(), name='list-marks'),
    path('marks/<int:pk>/', MarksDetail.as_view(), name='marks-detail'),

    path('marks/student/<int:studentId>/',
         MarkStudent.as_view(), name='marks-all-year'),
    path('marks/student/<int:studentId>/schoolyear/<int:school_year>/',
         MarksByYear.as_view(), name='marks-by-year'),
    path('marks/lecture/<int:lecture_id>/',
         MarksOfLecture.as_view(), name='marks-lecture'),

    path('marks/classes/<int:class_id>/schoolyear/<int:year_id>/',
         MarksOfClass.as_view(), name='marks-of-class'),

    path('marksregularys/', MarksRegularyView.as_view()),
    path('marksregularys/<int:pk>/', MarksRegularyDetail.as_view(),
         name='marksregulary-detail'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
