from django.urls import path

from .views import ResultListView, ResultCreateView, ResultUpdateView, ResultDeleteView, ResultDetailView

urlpatterns = [
    path("create/", ResultCreateView.as_view(), name="create-result"),
    path("edit-results/", ResultUpdateView.as_view() , name="edit-results"),
    # path("courses", DisplayRegisteredCoursesView.as_view(), name="display-registered-courses"),
    path("view/all", ResultListView.as_view(), name="view-results"),
    path("<int:pk>/", ResultDetailView.as_view(), name="result-detail")

]
