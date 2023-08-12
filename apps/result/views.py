from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student
from apps.corecode.models import Course

from .forms import CreateResults, EditResults
from .models import Result


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_result(request):
    students = Student.objects.all()
    if request.method == "POST":
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                courses = form.cleaned_data["courses"]
                session = form.cleaned_data["session"]
                semester = form.cleaned_data["semester"]
                selected_students = request.POST.getlist("students")  
                print(selected_students)
                results = []
                for student_id in selected_students:
                    stu = Student.objects.get(pk=student_id)
                    print(stu)
                    if stu.current_cohort:
                        for course in courses:
                            check = Result.objects.filter(
                                session=session,
                                semester=semester,
                                current_cohort=stu.current_cohort,
                                course=course,
                                student=stu,
                            ).first()
                            if not check:
                                results.append(
                                    Result(
                                        session=session,
                                        semester=semester,
                                        current_cohort=stu.current_cohort,
                                        course=course,
                                        student=stu,
                                    )
                                )
                Result.objects.bulk_create(results)
                return redirect("edit-results")

        # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "semester": request.current_semester,
                }
            )
            studentlist = ",".join(id_list)
            print(studentlist)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didn't select any student.")
    return render(request, "result/create_result.html", {"students": students})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_results(request):
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        results = Result.objects.filter(
            session=request.current_session, semester=request.current_semester
        )
        form = EditResults(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})


class ResultListView(LoginRequiredMixin, View):
        
    def get(self, request, *args, **kwargs):
        results = Result.objects.filter(
            session=request.current_session, semester=request.current_semester
        )
        bulk = {}

        for result in results:
            test_total = 0
            exam_total = 0
            total = test_total + exam_total
            gpa = 0
            courses = []
            for course in results:
                if course.student == result.student:
                    courses.append(course)
                    test_total += course.test_score
                    exam_total += course.exam_score
                    gpa += round(course.gpa() / len(courses), 3)

                

            bulk[result.student.id] = {
                "student": result.student,
                "courses": courses,
                "test_total": test_total,
                "exam_total": exam_total,
                "total_total": test_total + exam_total,
                "gpa": gpa,
            }

        context = {"results": bulk}
       
        return render(request, "result/all_results.html", context)
