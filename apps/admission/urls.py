from django.urls import path
from .views import AdmissionApplicationListView, AdmissionApplicationCreateView, AdmissionCycleListView, AdmissionCycleCreateView, AdmissionCycleUpdateView, AdmissionCycleDeleteView, AdmissionApplicationUpdateView, AdmissionApplicationDeleteView

urlpatterns = [
    path('list/', AdmissionCycleListView.as_view(), name='admission-cycle-list'),
    path('create/', AdmissionCycleCreateView.as_view(), name='admission-cycle-create'),
    path('update/<int:pk>/', AdmissionCycleUpdateView.as_view(), name='admission-cycle-update'),
    path('delete/<int:pk>/', AdmissionCycleDeleteView.as_view(), name='admission-cycle-delete'),
    path('application/list/', AdmissionApplicationListView.as_view(), name='admission-application-list'),
    path('application/create/', AdmissionApplicationCreateView.as_view(), name='admission-application-create'), 
    path('application/update/<int:pk>/', AdmissionApplicationUpdateView.as_view(), name='admission-application-update'),
    path('application/delete/<int:pk>/', AdmissionApplicationDeleteView.as_view(), name='admission-application-delete'),

]
