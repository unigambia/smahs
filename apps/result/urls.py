from django.urls import path

from .views import ResultListView, ResultCreateView, ResultEditView, ResultDeleteView, ResultDetailView, StudentResultListView, StudentListView, ResultUpdateView

urlpatterns = [
    path("create/", ResultCreateView.as_view(), name="create-result"),
    path("edit-result/<int:pk>/", ResultEditView.as_view() , name="edit-result"),
    path("edit-results", ResultUpdateView.as_view(), name="edit-results"),
    # path("courses", DisplayRegisteredCoursesView.as_view(), name="display-registered-courses"),
    path("view/all", ResultListView.as_view(), name="view-results"),
    path("<int:pk>/", ResultDetailView.as_view(), name="result-detail"),
    path("<int:pk>/delete/", ResultDeleteView.as_view(), name="delete-result"),
    path("student/<int:pk>/", StudentResultListView.as_view(), name="student-result-list"),
    path("student/list/", StudentListView.as_view(), name="student-list"),

]
