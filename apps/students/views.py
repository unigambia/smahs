import csv

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.finance.models import Invoice
from apps.corecode.models import Course, StudentCourse, CourseMaterial

from .models import Student, StudentBulkUpload

class StudentListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"

    def test_func(self):
        return self.request.user.is_superuser


class StudentDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(student=self.object)
        return context


class StudentCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = "__all__"
    success_message = "New student successfully added."

    def test_func(self):
        return self.request.user.is_superuser

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields.pop("user")
        return form
    
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if Student.objects.filter(email=email).exists():
            form.add_error("email", "Email already exists.")
            return self.form_invalid(form)
        return super(StudentCreateView, self).form_valid(form)


class StudentCourseMaterialView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = CourseMaterial
    template_name = "students/student_course_material.html"

    course_materials = CourseMaterial.objects.all()
    assignments = course_materials.get_assignments()
    lecture_notes = course_materials.get_lecture_notes()
    past_questions = course_materials.get_past_questions()
    other_materials = course_materials.get_other_materials()


    def test_func(self):
        return not self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["student"] = Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            context["student"] = None

        if self.object is not None:
            # Check if self.object is not None before accessing its attributes
            course_materials = CourseMaterial.objects.filter(course=self.object.course)
            context["assignments"] = course_materials.get_assignments()
            context["lecture_notes"] = course_materials.get_lecture_notes()
            context["past_questions"] = course_materials.get_past_questions()
            context["other_materials"] = course_materials.get_other_materials()
        else:
            # Handle the case where self.object is None
            context["assignments"] = []
            context["lecture_notes"] = []
            context["past_questions"] = []
            context["other_materials"] = []

        return context



    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None
    
    
class StudentUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
    success_message = "Record successfully updated."

    def test_func(self):
        return self.request.user.is_superuser

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['passport'].widget = widgets.FileInput()
        return form


class StudentDeleteView(UserPassesTestMixin, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")
    success_message = "Record successfully deleted."

    def test_func(self):
        return self.request.user.is_superuser


class StudentBulkUploadView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"

    def test_func(self):
        return self.request.user.is_superuser


class DownloadCSVViewdownloadcsv(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "mat_number",
                "surname",
                "firstname",
                "other_names",
                "gender",
                "parent_number",
                "address",
                "current_cohort",
            ]
        )

        return response

# student registered courses

class RegisteredCourseListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = StudentCourse
    template_name = "students/registered_courses.html"
    context_object_name = "student_courses"

    #not staff or superuser
    def test_func(self):
        return not self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return StudentCourse.objects.filter(student=student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = Student.objects.get(user=self.request.user)
        return context

