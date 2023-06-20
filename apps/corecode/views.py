from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    AcademicSessionForm,
    AcademicSemesterForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentCohortForm,
    CourseForm,
)
from .models import (
    AcademicSession,
    AcademicSemester,
    SiteConfig,
    StudentCohort,
    Course,
)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context


class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            semesters = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not semesters:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("session-list")
        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class SemesterListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSemester
    template_name = "corecode/semester_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSemesterForm()
        return context


class SemesterCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSemester
    form_class = AcademicSemesterForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("semesters")
    success_message = "New semester successfully added"


class SemesterUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSemester
    form_class = AcademicSemesterForm
    success_url = reverse_lazy("semesters")
    success_message = "Semester successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            semesters = (
                AcademicSemester.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not semesters:
                messages.warning(self.request, "You must set a semester to current.")
                return redirect("semester")
        return super().form_valid(form)


class SemesterDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSemester
    success_url = reverse_lazy("semesters")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The semester {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete semester as it is set to current")
            return redirect("semesters")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SemesterDeleteView, self).delete(request, *args, **kwargs)


class CohortListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentCohort
    template_name = "corecode/cohort_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentCohortForm()
        return context


class CohortCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentCohort
    form_class = StudentCohortForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("cohorts")
    success_message = "New cohort successfully added"


class CohortUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentCohort
    fields = ["name"]
    success_url = reverse_lazy("cohorts")
    success_message = "cohort successfully updated."
    template_name = "corecode/mgt_form.html"


class CohortDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentCohort
    success_url = reverse_lazy("cohorts")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The cohort {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(CohortDeleteView, self).delete(request, *args, **kwargs)


class CourseListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Course
    template_name = "corecode/course_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm()
        return context


class CourseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("courses")
    success_message = "New Course successfully added"


class CourseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ["name"]
    success_url = reverse_lazy("courses")
    success_message = "Course successfully updated."
    template_name = "corecode/mgt_form.html"


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy("courses")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The Course {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(CourseDeleteView, self).delete(request, *args, **kwargs)


class CurrentSessionAndSemesterView(LoginRequiredMixin, View):
    """Current SEssion and Semester"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.get(current=True),
                "current_semester": AcademicSemester.objects.get(current=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST,
            initial={
                "current_session": AcademicSession.objects.get(current=True),
                "current_semester": AcademicSemester.objects.get(current=True),
            }
        )
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            semester = form.cleaned_data["current_semestegr"]
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicSemester.objects.filter(name=semester).update(current=True)

        return render(request, self.template_name, {"form": form})
