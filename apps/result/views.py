from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, View, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML


from django.db import IntegrityError
from apps.students.models import Student
from .forms import EditResults, ResultForm
from .models import Result

    

class StudentResultListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Result
    template_name = "result/student_result_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(StudentResultListView, self).get_context_data(**kwargs)
        student = get_object_or_404(Student, id=self.kwargs["pk"])
        results = Result.objects.filter(student=student).order_by("session", "semester")
        
        # Preprocess results to group by session and semester
        grouped_results = {}
        total_points = 0
        total_courses = 0

        for result in results:
            session = result.session
            semester = result.semester
            if session not in grouped_results:
                grouped_results[session] = {}
            if semester not in grouped_results[session]:
                grouped_results[session][semester] = []
            grouped_results[session][semester].append(result)

            # Calculate total points and courses for GPA
            gpa_value = result.gpa()
            if gpa_value is not None:
                total_points += gpa_value
                total_courses += 1

        # Calculate the GPA
        gpa = round(total_points / total_courses, 2) if total_courses > 0 else "N/A"

        context["grouped_results"] = grouped_results
        context["student"] = student
        context["gpa"] = gpa
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
        # Filter results based on the logged-in student and order by session and semester
        return Result.objects.filter(student__user=self.request.user).order_by("session", "semester")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        results = self.get_queryset()

        # Calculate the GPA
        total_points = 0
        total_courses = 0
        for result in results:
            gpa_value = result.gpa()
            if gpa_value is not None:
                total_points += gpa_value
                total_courses += 1

        gpa = round(total_points / total_courses, 2) if total_courses > 0 else "N/A"

        context["student"] = student  # Add the student to the context
        context["gpa"] = gpa  # Add the GPA to the context
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
    

class ResultEditView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Result
    fields = ["student", "session", "semester", "course", "exam", "test_score", "exam_score"]
    success_url = reverse_lazy("student-result-list")
    success_message = "Result successfully updated."
    template_name = "corecode/mgt_form.html"

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_success_url(self):
        # Get the pk of the student from the result object
        student_pk = self.object.student.pk
        return reverse("student-result-list", kwargs={"pk": student_pk})
    
class ResultDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(id=kwargs["pk"])
        result.delete()
        messages.success(request, "Results successfully deleted")
        return redirect("result-list")
    
class DownloadResultView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        results = Result.objects.filter(student_id=student_id)
        student = Student.objects.get(pk=student_id)

        # Calculate the GPA
        total_points = 0
        total_courses = 0
        for result in results:
            gpa_value = result.gpa()
            if gpa_value is not None:
                total_points += gpa_value
                total_courses += 1

        gpa = round(total_points / total_courses, 2) if total_courses > 0 else "N/A"

        template = get_template('result/student_transcript.html')
        html_content = template.render({
            'results': results,
            'gpa': gpa,
            'student': {
                'name': student.firstname + ' ' + student.surname,
                'mat_number': student.mat_number,
                'year_enrolled': student.year_enrolled,
                'current_cohort': student.current_cohort,
            }
        })
        html = HTML(string=html_content, base_url=request.build_absolute_uri('/static/'))
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transcript.pdf"'
        return response