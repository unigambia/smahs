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
    ClassroomReservationCreateView,
    ClassroomReservationListView,
    ClassroomReservationUpdateView,
    ClassroomReservationDeleteView,
    ClassroomListView,
    ClassroomCreateView,
    ClassroomUpdateView,
    ClassroomDeleteView,
    EquipmentCheckoutListView,
    EquipmentCheckoutCreateView,
    EquipmentCheckoutUpdateView,
    EquipmentCheckoutDeleteView,
    EquipmentCreateView,
    EquipmentListView,
    EquipmentUpdateView,
    EquipmentDeleteView,
    AnnouncementCreateView,
    AnnouncementListView,
    AnnouncementUpdateView,
    AnnouncementDeleteView,
    AdminAlertCreateView,
    AdminAlertListView,
    AdminAlertUpdateView,
    AdminAlertDeleteView,
    LoginView,
    view_policies,
    access_procedures,
    download_guidelines,
    contact_support,
    it_help_desk,
    student_services,
    redirect_to_login,
    financial_aid,
    health_services,
    contact_details,
    career_services,
    advisors,
    
    )

urlpatterns = [
    
    path('login/', LoginView.as_view(), name='login'),
    path('', redirect_to_login, name='root_redirect'),
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
    # path('api/edit-event/', edit_event, name='edit-event'),
    # path('api/delete-event/', delete_event, name='delete-event'),

    path('event/<int:pk>/delete/', CalendarEventDeleteView.as_view(), name='event-delete'),
    path('api/calendar-events/', calendar_events_api, name='calendar-events-api'),

    
    #Classroom Reservation
    path('classroom-reservations/', ClassroomReservationListView.as_view(), name='classroom_reservations'),
    path('classroom-reservation/create/', ClassroomReservationCreateView.as_view(), name='classroom_reservation_create'),
    path('classroom-reservation/<int:pk>/update/', ClassroomReservationUpdateView.as_view(), name='classroom_reservation_update'),
    path('classroom-reservation/<int:pk>/delete/', ClassroomReservationDeleteView.as_view(), name='classroom_reservation_delete'),

    #Classroom

    path('classroom/', ClassroomListView.as_view(), name='classrooms'),
    path('classroom/create/', ClassroomCreateView.as_view(), name='classroom-create'),
    path('classroom/<int:pk>/update/', ClassroomUpdateView.as_view(), name='classroom-update'),
    path('classroom/<int:pk>/delete/', ClassroomDeleteView.as_view(), name='classroom-delete'),

    #Equipment Checkout

    path('equipment-checkout/', EquipmentCheckoutListView.as_view(), name='equipment-checkout'),
    path('equipment-checkout/create/', EquipmentCheckoutCreateView.as_view(), name='equipment-checkout-create'),
    path('equipment-checkout/<int:pk>/update/', EquipmentCheckoutUpdateView.as_view(), name='equipment-checkout-update'),
    path('equipment-checkout/<int:pk>/delete/', EquipmentCheckoutDeleteView.as_view(), name='equipment-checkout-delete'),   
    
    #Equipment

    path('equipment/', EquipmentListView.as_view(), name='equipments'),
    path('equipment/create/', EquipmentCreateView.as_view(), name='equipment-create'),
    path('equipment/<int:pk>/update/', EquipmentUpdateView.as_view(), name='equipment-update'),
    path('equipment/<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment-delete'),

    # Announcement

    path('announcement/', AnnouncementListView.as_view(), name='announcements'),
    path('announcement/create/', AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcement/<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement-delete'),

    # Admin Alert

    path('admin-alert/', AdminAlertListView.as_view(), name='admin-alerts'),
    path('admin-alert/create/', AdminAlertCreateView.as_view(), name='alert-create'),
    path('admin-alert/<int:pk>/update/', AdminAlertUpdateView.as_view(), name='alert-update'),
    path('admin-alert/<int:pk>/delete/', AdminAlertDeleteView.as_view(), name='alert-delete'),


    path('view-policies/', view_policies, name='view-policies'),
    path('access-procedures/', access_procedures, name='access-procedures'),
    path('download-guidelines/', download_guidelines, name='download-guidelines'),
    path('contact-support/', contact_support, name='contact-support'),
    path('it-help-desk/', it_help_desk, name='it-help-desk'),
    path('student-services/', student_services, name='student-services'),
    path('contacts/', contact_details, name='contact-details'),
    path('financial-aid/', financial_aid, name='financial-aid'),
    path('health-services/', health_services, name='health-services'),
    path('career-services/', career_services, name='career-services'),
    path('advisors/', advisors, name='advisors'),
    
    
]
