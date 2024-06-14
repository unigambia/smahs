from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, View, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from apps.corecode.forms import RegistrationForm, UserUpdateForm
from django.contrib.auth.decorators import user_passes_test
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import widgets, SelectMultiple



from .forms import (
    AcademicSessionForm,
    AcademicSemesterForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentCohortForm,
    CourseForm,
    AssignmentForm,
    ExamForm,
    DepartmentForm,
    ProgramForm,
    CourseRegistrationPeriodForm

)
from .models import (
    AcademicSession,
    AcademicSemester,
    SiteConfig,
    StudentCohort,
    Course,
    StudentCourse,
    CourseMaterial,
    Exam,
    Staff,
    Department,
    Program,
    CourseRegistrationPeriod


)
from apps.students.models import Student


class DashboardView(LoginRequiredMixin, TemplateView):
    
   def get_template_names(self):
        user = self.request.user
        if user.is_superuser:
            return "admin_dashboard.html"
        elif user.is_staff:
            return "lecturer_dashboard.html"
        else:
            return "student_dashboard.html"
    


class AdminDashboardView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        graduates = Student.objects.filter(current_status="graduate").count()
        context["graduates"] = graduates
        active_students = Student.objects.filter(current_status="active").count()
        context["active_students"] = active_students
        context["courses"] = Course.objects.all().count()
        context["sessions"] = AcademicSession.objects.all().count()
        context["semesters"] = AcademicSemester.objects.all().count()
        context["staffs"] = Staff.objects.all().count()
        context["users"] = User.objects.all().count()
        context["cohorts"] = StudentCohort.objects.all().count()
        context["assignments"] = CourseMaterial.objects.all().count()
        
        return context

class LecturerDashboardView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "lecturer_dashboard.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.filter(coordinator=self.request.user.staff).count()
        # context["students"] = StudentCourse.objects.filter(course__lecturer=self.request.user.staff).count()
        context["sessions"] = AcademicSession.objects.all().count()
        context["semesters"] = AcademicSemester.objects.all().count()
        return context

class StudentDashboardView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "student_dashboard.html"

    def test_func(self):
        return not self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        context["courses"] = StudentCourse.objects.filter(student=student).count()        
        context["sessions"] = AcademicSession.objects.all().count()
        context["semesters"] = AcademicSemester.objects.all().count()
        context["assignments"] = CourseMaterial.objects.filter(type="assignment").count()
        context["cohort_students"] = Student.objects.filter(current_cohort=self.request.user.student.current_cohort).count()

        return context    


class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        return render(self.template_name)

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
        try:
            obj = self.get_object()
        except AcademicSession.DoesNotExist:
            messages.error(request, "The session does not exist.")
            return redirect("sessions")

        # Check if the session is the current session
        if obj.current:
            messages.warning(request, "Cannot delete the current session.")
            return redirect("sessions")

        # Check if the session is linked to the current semester
        try:
            current_semester = AcademicSemester.objects.get(current=True)
            if current_semester.session == obj:
                messages.warning(request, "Cannot delete the session as it is linked to the current semester.")
                return redirect("sessions")
        except AcademicSemester.DoesNotExist:
            # No current semester found, safe to proceed
            pass

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
    fields = ["name", "code", "credit_unit", "level", "coordinator", "program"]
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

class CourseRegisterView(UserPassesTestMixin, LoginRequiredMixin, View):
    """Course Register View"""

    template_name = "corecode/course_register.html"
    form_class = CourseForm

    def test_func(self):
        # not staff or superuser
        return not self.request.user.is_staff or self.request.user.is_superuser

    def get_course_registration_status(self):
        current_period = CourseRegistrationPeriod.objects.filter(status=True).first()
        return current_period is not None

    def get(self, request, *args, **kwargs):
        registration_open = self.get_course_registration_status()
        form = self.form_class()
        courses = Course.objects.all()
        user = request.user
        student = get_object_or_404(Student, user=user)
        registered_courses = StudentCourse.objects.filter(student=student).values_list('course_id', flat=True)

        return render(request, self.template_name, {
            "form": form,
            "courses": courses,
            "student": student,
            "registered_courses_ids": registered_courses,
            "registration_open": registration_open
        })

    def post(self, request, *args, **kwargs):
        if not self.get_course_registration_status():
            messages.error(request, "Course registration is currently closed.")
            return redirect("home")  # Redirect to home or another appropriate page

        course_id = request.POST.get("course_id")
        session = request.current_session
        semester = request.current_semester
        student = get_object_or_404(Student, user=request.user)

        if course_id:
            course = get_object_or_404(Course, id=course_id)

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
        return  self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm()
        return context

    def get_queryset(self):
        return Course.objects.filter(coordinator=self.request.user.    is_staff)
    
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
    
    
class AssignmentsCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "corecode/mgt_form.html"
    model = CourseMaterial
    fields = "__all__"
    success_message = "New Assignment successfully added."

    def test_func(self):
        return self.request.user.is_staff   

    def get_form(self):
        """add date picker in forms"""
        form = super(AssignmentsCreateView, self).get_form()
        form.fields["due_date"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields.pop("course")
        form.fields.pop("academic_session")
        form.fields.pop("academic_semester")
        form.fields.pop("date_created")
        form.fields.pop("lecturer")
        return form
    
    def form_valid(self, form: BaseForm) -> HttpResponse:
        form.instance.coordinator = self.request.user.staff
        form.instance.course = Course.objects.get(id=self.kwargs["course_id"])
        form.instance.academic_session = AcademicSession.objects.get(current=True)
        form.instance.academic_semester = AcademicSemester.objects.get(current=True)
        form.instance.file = self.request.FILES.get("file")

        return super().form_valid(form)
    
    def get_success_url(self):
        from django.urls import reverse
        return reverse("staff-course-assignments", kwargs={"pk": self.kwargs["course_id"]})


class AssignmentsListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = CourseMaterial
    template_name = "corecode/assignments.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_id"] = self.kwargs["pk"]
        context["course_name"] = Course.objects.get(pk=self.kwargs["pk"]).name
        return context

    def get_queryset(self):
        return CourseMaterial.objects.filter(course=self.kwargs["pk"])

class AssignmentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = CourseMaterial
    form_class = AssignmentForm
    template_name = "corecode/mgt_form.html"
    success_message = "The Assignment for course '{}' has been updated"

    def get_success_url(self):
        return reverse_lazy("staff-course-assignments", kwargs={'pk': self.kwargs['course_id']})

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.staff = self.request.user.staff
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        form.instance.course = course
        form.instance.academic_session = AcademicSession.objects.get(current=True)
        form.instance.academic_semester = AcademicSemester.objects.get(current=True)
        form.instance.coordinator = self.request.user.staff  # Set the lecturer

        uploaded_file: InMemoryUploadedFile = form.cleaned_data['file']
        
        if uploaded_file:
            # Set the file field of the Assignment instance
            form.instance.file = uploaded_file


        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        course = Course.objects.get(id=self.kwargs["course_id"])
        return self.success_message.format(course.name)
    

class AssignmentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = CourseMaterial
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The Assignment for course '{}' has been deleted"

    def get_success_url(self):
        return reverse_lazy("staff-course-assignments", kwargs={'pk': self.kwargs['course_id']})

    def test_func(self):
        return self.request.user.is_staff

    def get_success_message(self, cleaned_data):
        course = Course.objects.get(id=self.kwargs["course_id"])
        return self.success_message.format(course.name)


#Exam View

class ExamsCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "corecode/mgt_form.html"
    model = Exam
    form_class = ExamForm  # Using the form class directly
    success_message = "New Exam successfully added."

    def test_func(self):
        return self.request.user.is_superuser   
    
    def get_success_url(self):
        return reverse("exams-list")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop("date_created")
        return form
    
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        return response

class ExamsListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Exam
    template_name = "corecode/exams_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Exam.objects.all()
class ExamUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = "corecode/mgt_form.html"
    success_message = "The Exam for course '{}' has been updated"

    def get_success_url(self):
        return reverse_lazy("exams-list")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        uploaded_file: InMemoryUploadedFile = form.cleaned_data['file']
        if uploaded_file:
            # Set the file field of the Exam instance
            form.instance.file = uploaded_file

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message.format(self.object.title)

class ExamDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The Exam for course '{}' has been deleted"

    def get_success_url(self):
        return reverse_lazy("exams-list")

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.title))
        return super().delete(request, *args, **kwargs) 
    

# Department View
    
class DepartmentListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Department
    template_name = "corecode/department_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DepartmentForm()
        return context

    
class DepartmentCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("departments")
    success_message = "New Department successfully added"

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        obj = self.object
        return super().form_valid(form)
    
class DepartmentUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Department
    form_class = DepartmentForm
    success_url = reverse_lazy("departments")
    success_message = "Department successfully updated."
    template_name = "corecode/mgt_form.html"

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        obj = self.object
        return super().form_valid(form)
class DepartmentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Department
    success_url = reverse_lazy("departments")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The Department {} has been deleted with all its attached content"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(DepartmentDeleteView, self).delete(request, *args, **kwargs)
    

# Program View
    
class ProgramListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Program
    template_name = "corecode/program_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProgramForm()
        return context
    

class ProgramCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("programs")
    success_message = "New Program successfully added"

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        obj = self.object
        return super().form_valid(form)
    

class ProgramUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser
    
    model = Program
    form_class = ProgramForm

    success_url = reverse_lazy("programs")
    success_message = "Program successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        return super().form_valid(form)
    

class ProgramDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Program
    success_url = reverse_lazy("programs")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The Program {} has been deleted with all its attached content"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ProgramDeleteView, self).delete(request, *args, **kwargs)
    


class CourseRegistrationPeriodListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = CourseRegistrationPeriod
    template_name = "corecode/course_registration_period_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CourseRegistrationPeriodForm()
        return context

    def get_queryset(self):
        return CourseRegistrationPeriod.objects.all()
    

class CourseRegistrationPeriodCreateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CourseRegistrationPeriod
    form_class = CourseRegistrationPeriodForm
    template_name = "corecode/mgt_form.html"
    success_message = "New course registration period successfully added."

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy("course-registration-periods")

    def form_valid(self, form):
        obj = self.object
        return super().form_valid(form)
    


class CourseRegistrationPeriodUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CourseRegistrationPeriod
    form_class = CourseRegistrationPeriodForm
    template_name = "corecode/mgt_form.html"
    success_message = "Course registration period successfully updated."

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy("course-registration-periods")

    def form_valid(self, form):
        obj = self.object
        return super().form_valid(form)
    

class CourseRegistrationPeriodDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = CourseRegistrationPeriod
    success_url = reverse_lazy("course-registration-periods")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The course registration period has been deleted"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message)
        return super(CourseRegistrationPeriodDeleteView, self).delete(request, *args, **kwargs)