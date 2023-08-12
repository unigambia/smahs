from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from apps.corecode.forms import RegistrationForm, UserUpdateForm
from django.contrib.auth.decorators import user_passes_test



from .forms import (
    AcademicSessionForm,
    AcademicSemesterForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentCohortForm,
    CourseForm,
    UserForm,
)
from .models import (
    AcademicSession,
    AcademicSemester,
    SiteConfig,
    StudentCohort,
    Course,
    StudentCourse

)
from apps.students.models import Student



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


class SessionListView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"


    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context
    
class SessionCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context

class SessionUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def test_func(self):
        return self.request.user.is_superuser

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


class SessionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class SemesterListView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSemester
    template_name = "corecode/semester_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSemesterForm()
        return context


class SemesterCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSemester
    form_class = AcademicSemesterForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("semesters")
    success_message = "New semester successfully added"

    def test_func(self):
        return self.request.user.is_superuser

class SemesterUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSemester
    form_class = AcademicSemesterForm
    success_url = reverse_lazy("semesters")
    success_message = "Semester successfully updated."
    template_name = "corecode/mgt_form.html"

    def test_func(self):
        return self.request.user.is_superuser

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


class SemesterDeleteView(UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = AcademicSemester
    success_url = reverse_lazy("semesters")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The semester {} has been deleted with all its attached content"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete semester as it is set to current")
            return redirect("semesters")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SemesterDeleteView, self).delete(request, *args, **kwargs)


class CohortListView(UserPassesTestMixin,LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentCohort
    template_name = "corecode/cohort_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentCohortForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser

class CohortCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentCohort
    form_class = StudentCohortForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("cohorts")
    success_message = "New cohort successfully added"

    def test_func(self):
        return self.request.user.is_superuser

class CohortUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentCohort
    fields = ["name"]
    success_url = reverse_lazy("cohorts")
    success_message = "cohort successfully updated."
    template_name = "corecode/mgt_form.html"

    def test_func(self):
        return self.request.user.is_superuser


class CohortDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = StudentCohort
    success_url = reverse_lazy("cohorts")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The cohort {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(CohortDeleteView, self).delete(request, *args, **kwargs)
    
    def test_func(self):
        return self.request.user.is_superuser


class CourseListView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Course
    template_name = "corecode/course_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm()
        return context
    
    def test_func(self):
        return self.request.user.is_superuser


class CourseCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("courses")
    success_message = "New Course successfully added"

    def test_func(self):
        return self.request.user.is_superuser


class CourseUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ["name", "code", "credit_unit", "level", "lecturer"]
    success_url = reverse_lazy("courses")
    success_message = "Course successfully updated."
    template_name = "corecode/mgt_form.html"

    def test_func(self):
        return self.request.user.is_superuser


class CourseDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy("courses")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The Course {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(CourseDeleteView, self).delete(request, *args, **kwargs)
    
    def test_func(self):
        return self.request.user.is_superuser


class CurrentSessionAndSemesterView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Current SEssion and Semester"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def test_func(self):
        return self.request.user.is_superuser

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

class CourseRegisterView(UserPassesTestMixin,LoginRequiredMixin, View):
    """Course Register View"""

    template_name = "corecode/course_register.html"
    form_class = CourseForm

    def test_func(self):
        #not staff or superuser
        return not self.request.user.is_staff or self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        courses = Course.objects.all()
        user = request.user
        student = Student.objects.get(user=user)
        registered_courses = StudentCourse.objects.filter(student=student).values_list('course_id', flat=True)
        
        return render(request, self.template_name, {"form": form, "courses": courses, "registered_courses_ids": registered_courses})

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_id")
        session = request.current_session
        semester = request.current_semester
        student = Student.objects.get(user=request.user)
        
        if course_id:
            course = Course.objects.get(id=course_id)
            
            # Create or update StudentCourse instance with session and semester
            student_course, created = StudentCourse.objects.get_or_create(
                student=student,
                course=course,
                academic_session=session,
                academic_semester=semester
            )
            
            if not created:
                student_course.delete()  # Remove the relationship
                messages.success(request, "Course unregistration successful.")
            else:
                messages.success(request, "Course registration successful.")

        return redirect("course-registration")


class UnregisterCourseView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Unregister Course View"""


    def test_func(self):
        return not self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_id")
        
        if course_id:
            student = request.user.student
            course = get_object_or_404(Course, id=course_id)
            
            try:
                student_course = StudentCourse.objects.get(student=student, course=course)
                student_course.delete()  # Remove the relationship
                messages.success(request, "Course unregistration successful.")
            except StudentCourse.DoesNotExist:
                messages.error(request, "You are not registered for this course.")
                
        return redirect("course-registration")
    

# class view for staff to view all courses assigned to them

class StaffCourseListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Course
    template_name = "corecode/staff_course_list.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm()
        return context

    def get_queryset(self):
        return Course.objects.filter(lecturer=self.request.user.staff)
    
# show registered students for the staff course

class CourseRegisteredStudentsView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = StudentCourse
    template_name = "corecode/course_registered_students.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_name"] = Course.objects.get(pk=self.kwargs["pk"]).name
        return context

    def get_queryset(self):
        return StudentCourse.objects.filter(course=self.kwargs["pk"])
