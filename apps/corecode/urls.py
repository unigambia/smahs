from django.urls import path

from .views import (
    CohortCreateView,
    CohortDeleteView,
    CohortListView,
    CohortUpdateView,
    CurrentSessionAndSemesterView,
    IndexView,
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
)

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
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
    path(
        "course/<int:pk>/update/",
        CourseUpdateView.as_view(),
        name="course-update",
    ),
    path(
        "course/<int:pk>/delete/",
        CourseDeleteView.as_view(),
        name="course-delete",
    ),
]
