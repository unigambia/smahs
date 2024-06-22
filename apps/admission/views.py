from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import AdmissionCycle, AdmissionApplication
from .forms import AdmissionCycleForm, AdmissionApplicationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class AdmissionCycleListView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AdmissionCycle
    template_name = 'admissions/admission_cycle_list.html'
    context_object_name = 'admission_cycles'
    success_message = 'Admission cycle deleted successfully'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['form'] = AdmissionCycleForm()
        return context
class AdmissionCycleCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AdmissionCycle
    form_class = AdmissionCycleForm
    template_name = 'corecode/mgt_form.html'
    success_message = 'Admission cycle created successfully'

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save()
        return redirect('admission-cycle-list')

class AdmissionCycleUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AdmissionCycle
    form_class = AdmissionCycleForm
    template_name = 'corecode/mgt_form.html'
    success_message = 'Admission cycle updated successfully'

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save()
        return redirect('admission-cycle-list')
    
class AdmissionCycleDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AdmissionCycle
    template_name = 'corecode/mgt_confirm_delete.html'
    success_url = '/admissions/list/'
    success_message = 'Admission cycle deleted successfully'

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AdmissionCycleDeleteView, self).delete(request, *args, **kwargs)

class AdmissionApplicationListView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AdmissionApplication
    template_name = 'admissions/admission_application_list.html'
    context_object_name = 'admission_applications'
    success_message = 'Admission application deleted successfully'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['applications'] = AdmissionApplication.objects.all()
        context['form'] = AdmissionApplicationForm()
        return context
    
class AdmissionApplicationCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AdmissionApplication
    form_class = AdmissionApplicationForm
    template_name = 'corecode/mgt_form.html'
    success_message = 'Admission application created successfully'
    success_url = reverse_lazy('admission-application-list')

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
class AdmissionApplicationUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AdmissionApplication
    form_class = AdmissionApplicationForm
    template_name = 'corecode/mgt_form.html'    
    success_message = 'Admission application updated successfully'

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.save()
        return redirect('admission-application-list')
    
class AdmissionApplicationDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AdmissionApplication
    template_name = 'corecode/mgt_confirm_delete.html'
    success_url = '/admissions/application/list/'
    success_message = 'Admission application deleted successfully'

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AdmissionApplicationDeleteView, self).delete(request, *args, **kwargs)