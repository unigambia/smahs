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
        form.fields.pop("created_by")
        form.fields.pop("updated_by")
        return form
    
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if Staff.objects.filter(email=email).exists():
            form.add_error("email", "Email already exists.")
            return self.form_invalid(form)
        return super(StaffCreateView, self).form_valid(form)


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
        form.fields.pop("created_by")
        form.fields.pop("updated_by")
        return form


class StaffDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")
    success_message = "Record successfully deleted."

    def test_func(self):
        return self.request.user.is_superuser

