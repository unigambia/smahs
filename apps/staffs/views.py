from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Staff


class StaffListView(ListView):
    model = Staff


class StaffDetailView(DetailView):
    model = Staff
    template_name = "staffs/staff_detail.html"


class StaffCreateView(UserPassesTestMixin, LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Staff
    fields = "__all__"
    success_message = "New staff successfully added"

    def test_func(self):
        return self.request.user.is_superuser   

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_employment"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields.pop("user")
        return form


class StaffUpdateView(UserPassesTestMixin, LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Staff
    fields = "__all__"
    success_message = "Record successfully updated."

    def test_func(self):
        return self.request.user.is_superuser

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_employment"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class StaffDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")
    success_message = "Record successfully deleted."

    def test_func(self):
        return self.request.user.is_superuser

