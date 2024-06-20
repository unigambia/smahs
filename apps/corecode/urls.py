from django.urls import path

from .views import (
    CohortCreateView,
    CohortDeleteView,
    CohortListView,
    CohortUpdateView,
    CurrentSessionAndSemesterView,
    SessionCreateView,
    SessionDeleteView,
    SessionListView,
    SessionUpdateView,
    SiteConfigView,
    CourseCreateView,
    CourseDeleteView,
    CourseListView,
    CourseUpdateView,
    SemesterCreateView,
    SemesterDeleteView,
    SemesterListView,
    SemesterUpdateView,
    CourseRegisterView,
    UnregisterCourseView,
    StaffCourseListView,
    CourseRegisteredStudentsView,
    AssignmentsCreateView,
    AssignmentsListView,
    AssignmentUpdateView,
    AssignmentDeleteView,
    ExamsCreateView,
    ExamsListView,
    ExamUpdateView,
    ExamDeleteView,
    AdminDashboardView,
    LecturerDashboardView,
    StudentDashboardView,
    DashboardView,
    DepartmentCreateView,
    DepartmentListView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    ProgramCreateView,
    ProgramListView,
    ProgramUpdateView,
    ProgramDeleteView,
    CourseRegistrationPeriodListView,
    CourseRegistrationPeriodUpdateView,
    CourseRegistrationPeriodCreateView,
    CourseRegistrationPeriodDeleteView,
    ScheduleManagementView,
    ScheduleCreateView,
    ScheduleUpdateView,
    ScheduleDeleteView,
    CalendarEventListView,
    CalendarEventCreateView,
    CalendarEventUpdateView,
    CalendarEventDeleteView,
    calendar_events_api,
    edit_event,
    delete_event
    

    )

urlpatterns = [
    
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/dashboard", AdminDashboardView.as_view(), name="admin"),
    path("lecturer/dashboard", LecturerDashboardView.as_view(), name="lecturer"),
    path("student/dashboard", StudentDashboardView.as_view(), name="student"),

    path("site-config", SiteConfigView.as_view(), name="configs"),
    path(
        "current-session/", CurrentSessionAndSemesterView.as_view(), name="current-session"
    ),
    path("session/list/", SessionListView.as_view(), name="sessions"),
    path("session/create/", SessionCreateView.as_view(), name="session-create"),
    path(
        "session/<int:pk>/update/",
        SessionUpdateView.as_view(),
        name="session-update",
    ),
    path(
        "session/<int:pk>/delete/",
        SessionDeleteView.as_view(),
        name="session-delete",
    ),
    path("semester/list/", SemesterListView.as_view(), name="semesters"),
    path("semester/create/", SemesterCreateView.as_view(), name="semesters-create"),
    path("semester/<int:pk>/update/", SemesterUpdateView.as_view(), name="semester-update"),
    path("semester/<int:pk>/delete/", SemesterDeleteView.as_view(), name="semester-delete"),
    path("cohort/list/", CohortListView.as_view(), name="cohorts"),
    path("cohort/create/", CohortCreateView.as_view(), name="cohorts-create"),
    path("cohort/<int:pk>/update/", CohortUpdateView.as_view(), name="cohorts-update"),
    path("cohort/<int:pk>/delete/", CohortDeleteView.as_view(), name="cohorts-delete"),
    path("course/list/", CourseListView.as_view(), name="courses"),
    path("course/create/", CourseCreateView.as_view(), name="course-create"),
    path('course/register/', CourseRegisterView.as_view(), name='course-registration'),
    
    path("course/<int:pk>/update/", CourseUpdateView.as_view(),name="course-update"),
    path("course/<int:pk>/delete/", CourseDeleteView.as_view(), name="course-delete"),
    path('course/unregister/', UnregisterCourseView.as_view(), name='course-unregistration'),
    path('staff/class/', StaffCourseListView.as_view(), name='staff-courses'),
    path('staff/class/<int:pk>', CourseRegisteredStudentsView.as_view(), name='staff-course-students'),
    path('staff/class/<int:pk>/assignment', AssignmentsListView.as_view(), name='staff-course-assignments'),
    path('staff/class/<int:course_id>/assignment/create', AssignmentsCreateView.as_view(), name='staff-course-assignments-create'),
    path('staff/class/<int:course_id>/assignment/<int:pk>/update', AssignmentUpdateView.as_view(), name='staff-course-assignments-update'),
    path('staff/class/<int:course_id>/assignment/<int:pk>/delete', AssignmentDeleteView.as_view(), name='staff-course-assignments-delete'),

    #exam
    path('exam/list', ExamsListView.as_view(), name='exams-list'),
    path('exam/create', ExamsCreateView.as_view(), name='exam-create'),
    path('exam/<int:pk>/update', ExamUpdateView.as_view(), name='exam-update'),
    path('exam/<int:pk>/delete', ExamDeleteView.as_view(), name='exam-delete'),

    #department

    path('department/list', DepartmentListView.as_view(), name='departments'),
    path('department/create', DepartmentCreateView.as_view(), name='department-create'),
    path('department/<int:pk>/update', DepartmentUpdateView.as_view(), name='department-update'),
    path('department/<int:pk>/delete', DepartmentDeleteView.as_view(), name='department-delete'),

    #program

    path('program/list', ProgramListView.as_view(), name='programs'),
    path('program/create', ProgramCreateView.as_view(), name='program-create'),
    path('program/<int:pk>/update', ProgramUpdateView.as_view(), name='program-update'),
    path('program/<int:pk>/delete', ProgramDeleteView.as_view(), name='program-delete'),

    #course registration period

    path('course-registration-period/list', CourseRegistrationPeriodListView.as_view(), name='course-registration-periods'),
    path('course-registration-period/create', CourseRegistrationPeriodCreateView.as_view(), name='course-registration-period-create'),
    path('course-registration-period/<int:pk>/update', CourseRegistrationPeriodUpdateView.as_view(), name='course-registration-period-update'),
    path('course-registration-period/<int:pk>/delete', CourseRegistrationPeriodDeleteView.as_view(), name='course-registration-period-delete'),
    
    #Schedule Management

    path('schedule/', ScheduleManagementView.as_view(), name='schedules'),
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedule/<int:pk>/update/', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedule/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
 
   #Calendar Event

    path('events/', CalendarEventListView.as_view(), name='event-list'),
    path('event/create/', CalendarEventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/update/', CalendarEventUpdateView.as_view(), name='event-update'),
    path('api/edit-event/', edit_event, name='edit-event'),
    path('api/delete-event/', delete_event, name='delete-event'),

    path('event/<int:pk>/delete/', CalendarEventDeleteView.as_view(), name='event-delete'),
    path('api/calendar-events/', calendar_events_api, name='calendar-events-api'),

    

    

    
]
