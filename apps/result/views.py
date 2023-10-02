from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView
from django.urls import reverse_lazy

from apps.students.models import Student
from apps.corecode.models import Course, StudentCourse, AcademicSemester, AcademicSession

from .forms import CreateResults, EditResults
from .models import Result

    
# class ResultDetailView(LoginRequiredMixin, DetailView):
#     model = Result
#     template_name = "result/create_result2.html"

class ResultListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Result
    template_name = "result/result_list.html"

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(ResultListView, self).get_context_data(**kwargs)
        context["results"] = Result.objects.all()
        return context

class ResultDetailView(LoginRequiredMixin, DetailView):
    model = Result
    template_name = "result/result_detail.html"
    context_object_name = "result"

    def get_context_data(self, **kwargs):
        context = super(ResultDetailView, self).get_context_data(**kwargs)
        result = context["result"]

        # Retrieve the associated student based on the id
        student_id = result.student.id  # Assuming result.student is the Student object
        student = Student.objects.get(pk=student_id)

        # Fetch all results for the same student
        student_results = Result.objects.filter(student=student).order_by("session", "semester")

        # Organize results into a structured format
        structured_results = {}
        current_session = None

        if not student_results:
            context["no_results_message"] = "No results found for this student."


        for student_result in student_results:
            if student_result.session != current_session:
                structured_results[student_result.session] = {}
                current_session = student_result.session

            session_dict = structured_results[student_result.session]
            if student_result.semester not in session_dict:
                session_dict[student_result.semester] = []

            session_dict[student_result.semester].append(student_result)

        context["structured_results"] = structured_results
        context["student"] = student  # Add the student to the context
        return context
    

class ResultCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin ,CreateView):
    model = Result
    template_name = 'result/create_result.html'  
    fields = "__all__"
    success_url = reverse_lazy("create-result")
    success_message = "Added Result Successfully"

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        # Check if a result with the same session and semester already exists
        session = form.cleaned_data['session']
        semester = form.cleaned_data['semester']
        student = form.cleaned_data['student']

        existing_result = Result.objects.filter(session=session, semester=semester, student=student).exists()
        
        if existing_result:
            # Return an error message if a duplicate result exists
            form.add_error(None, "A result for this session and semester already exists for the student.")
            return self.form_invalid(form)
        
        return super().form_valid(form)


    

class ResultUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Result
    template_name = 'result/edit_results.html'  
    fields = "__all__"
    success_url = reverse_lazy("create-result")
    success_message = "Updated Result Successfully"

    def test_func(self):
        return self.request.user.is_superuser

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
