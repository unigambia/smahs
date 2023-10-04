from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from apps.students.models import Student
from apps.corecode.models import Course, StudentCourse, AcademicSemester, AcademicSession
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateResults, EditResults, ResultForm
from .models import Result

    
# class ResultDetailView(LoginRequiredMixin, DetailView):
#     model = Result
#     template_name = "result/create_result2.html"

# class ResultListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
#     model = Result
#     template_name = "result/result_list.html"

#     def test_func(self):
#         return self.request.user.is_superuser
    
#     def get_queryset(self):
#         # Filter the results by the student ID passed in the URL
#         student_id = self.kwargs['student_id']
#         return Result.objects.filter(student__id=student_id)
    
#     def get_context_data(self, **kwargs):
#         context = super(ResultListView, self).get_context_data(**kwargs)
#         context["student"] = get_object_or_404(Student, id=self.kwargs['student_id'])
#         return context


    
# student result list view

class StudentResultListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Result
    template_name = "result/student_result_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(StudentResultListView, self).get_context_data(**kwargs)
        student = get_object_or_404(Student, id=self.kwargs["pk"])
        print(self.kwargs["pk"])
        print(student)
        context["results"] = Result.objects.filter(student=student)
        context["student"] = student
        return context

# student list view

class ResultStudentListView(LoginRequiredMixin, ListView, UserPassesTestMixin):
    model = Student
    template_name = "result/student_list.html"

    def get_context_data(self, **kwargs):
        context = super(ResultStudentListView, self).get_context_data(**kwargs)
        context["students"] = Student.objects.all()
        return context
    
class StudentResultsListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = "result/student_results_list.html"
    context_object_name = "results"

    def get_queryset(self):
        # Filter results based on the logged-in student
        return Result.objects.filter(student__user=self.request.user).order_by("session", "semester")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        context["student"] = student  # Add the student to the context
        return context


class ResultCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Result
    template_name = 'result/create_result.html'
    form_class = ResultForm
    
    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy("student-result-list", kwargs={"pk": self.object.student.id})

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Result added successfully!")
            return response
        except IntegrityError:
            form.add_error(None, "A result for this combination of student, session, semester, and course already exists!")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in the form.")
        return render(self.request, self.template_name, {'form': form})
    

# class ResultUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Result
#     template_name = 'result/edit_results.html'  
#     fields = "__all__"
#     success_message = "Updated Result Successfully"

#     def test_func(self):
#         return self.request.user.is_superuser
    
#     def get_success_url(self):
#         return reverse_lazy("student-result-list", kwargs={"pk": self.object.student.id})

# class DisplayRegisteredCoursesView(LoginRequiredMixin, UserPassesTestMixin, View):
#     def test_func(self):
#         return self.request.user.is_superuser

#     def get(self, request, *args, **kwargs):
#         student_ids = self.request.GET.getlist("students")
#         students = Student.objects.filter(id__in=student_ids)

#         students_registered_courses = {}  # Dictionary to store registered courses
#         for student in students:
#             student_courses = StudentCourse.objects.filter(student=student)
#             print(student_courses)
#             registered_courses = [student_course.course for student_course in student_courses]
#             print(registered_courses)
#             students_registered_courses[student.id] = registered_courses
#             print(students_registered_courses[student.id]   )

#         form = CreateResults()  # Create an instance of the form
#         available_sessions = AcademicSession.objects.all()
#         available_semesters = AcademicSemester.objects.all()


#         return render(
#             request,
#             "result/display_registered_courses.html",
#             {
#                 "students": students,
#                 "form": form,
#                 "students_registered_courses": students_registered_courses,
#                 "count": len(students),
#                 "session": available_sessions,
#                 "semester": available_semesters,
#             },
#         )


class ResultEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Result
    template_name = "result/edit_results.html"
    form_class = EditResults
    success_message = "Updated Result Successfully"

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_success_url(self):
        return reverse_lazy("edit-result", kwargs={"pk": self.kwargs["pk"]})

    
    def get(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        form = ResultForm(instance=result)
        return render(request, self.template_name, {"form": form, "student": result.student})

    def post(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        if "delete" in request.POST:
            result.delete()
            messages.success(request, "Result deleted successfully.")
            return redirect(self.get_success_url())

        form = ResultForm(request.POST, instance=result)

        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.get_success_url())
        else:    
            return render(request, self.template_name, {"form": form})


class ResultDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        result.delete()
        messages.success(request, "Results successfully deleted")
        return redirect("result-list")

