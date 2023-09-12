from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, reverse
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student
from apps.corecode.models import Course, StudentCourse, AcademicSemester, AcademicSession

from .forms import CreateResults, EditResults
from .models import Result


class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = "result/result_list.html"

    def get_queryset(self):
        return Result.objects.filter(
            session=self.request.current_session,
            semester=self.request.current_semester,
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.filter(
            session=self.request.current_session,
            semester=self.request.current_semester,
        )
        return context
    

class ResultDetailView(LoginRequiredMixin, DetailView):
    model = Result
    template_name = "result/create_result2.html"

class ResultCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        form = CreateResults()
        students = Student.objects.all()  # Get the list of all students
        return render(request, "result/create_result.html", {"form": form, "students": students})

    def post(self, request, *args, **kwargs):
        form = CreateResults(request.POST)
        selected_student_ids = [int(id) for id in request.POST.getlist("students")]
        students = Student.objects.filter(id__in=selected_student_ids)

        if not students:
            messages.warning(request, "No students selected.")
            return redirect("create-result")

        # ... (get registered courses for each student)

        # Redirect to the new view for displaying registered courses
        query_string = "&".join([f"students={id}" for id in selected_student_ids])
        redirect_url = reverse("display-registered-courses") + "?" + query_string
        return redirect(redirect_url)
    

class ResultUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        form = CreateResults(instance=result)
        return render(request, "result/create_result.html", {"form": form})

    def post(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        form = CreateResults(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("result-detail", kwargs["pk"])
        return render(request, "result/create_result.html", {"form": form})

class DisplayRegisteredCoursesView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        student_ids = self.request.GET.getlist("students")
        students = Student.objects.filter(id__in=student_ids)

        students_registered_courses = {}  # Dictionary to store registered courses
        for student in students:
            student_courses = StudentCourse.objects.filter(student=student)
            registered_courses = [student_course.course for student_course in student_courses]
            students_registered_courses[student.id] = registered_courses

        form = CreateResults()  # Create an instance of the form
        available_sessions = AcademicSession.objects.all()
        available_semesters = AcademicSemester.objects.all()


        return render(
            request,
            "result/display_registered_courses.html",
            {
                "students": students,
                "registered_courses": students_registered_courses,
                "form": form,
                "count": len(students),
                "session": available_sessions,
                "semester": available_semesters,
            },
        )


    

class ResultEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        form = EditResults(instance=result)
        return render(request, "result/edit_results.html", {"form": form})

    def post(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        form = EditResults(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("result-detail", kwargs["pk"])
        return render(request, "result/edit_results.html", {"form": form})
    


class ResultDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        result.delete()
        messages.success(request, "Results successfully deleted")
        return redirect("result-list")
