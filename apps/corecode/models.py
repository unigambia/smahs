from django.db import models
from ..staffs.models import Staff
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from enum import Enum

# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='session_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='session_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicSemester(models.Model):
    """Academic Semester"""

    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, default=1)
    current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='semester_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='semester_updated_by', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class StudentCohort(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='cohort_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='cohort_updated_by', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name = "Cohort"
        verbose_name_plural = "Cohorts"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    """Course"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True , null=True)
    credit_unit = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='course_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='course_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    coordinator  = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordinator",
    )
    program = models.ForeignKey('Program', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class StudentCourse(models.Model):
    from apps.students.models import Student
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='course_registration_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='course_registration_updated_by', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        unique_together = ['student', 'course', 'academic_session', 'academic_semester']

    # def __str__(self):
    #     return f"{self.student.surname} registered for {self.course.name} on {self.registration_date} in {self.academic_session}"

class CourseMaterialQuerySet(models.QuerySet):
    def get_assignments(self):
        return self.filter(type="assignment")

    def get_lecture_notes(self):
        return self.filter(type="lecture_note")

    def get_past_questions(self):
        return self.filter(type="past_question")

    def get_other_materials(self):
        return self.filter(type="others")
    

class CourseMaterialManager(models.Manager):
    def get_queryset(self):
        return CourseMaterialQuerySet(self.model, using=self._db)

class CourseMaterial(models.Model):
    """Assignments"""
    CHOICES = (
        ("assignment", "Assignment"),
        ("lecture_note", "Lecture Note"),
        ("past_question", "Past Question"),
        ("others", "Others")
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="assignments", null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    total_marks = models.IntegerField(default=0, null=True, blank=True)
    type = models.CharField(max_length=20, choices=CHOICES, default="assignment")
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='course_material_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='course_material_updated_by', null=True, blank=True, on_delete=models.SET_NULL)
    lecturer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lecturer_assignment",
    )
    def __str__(self):
        return self.title

    objects = CourseMaterialManager()
   
    class Meta:
        ordering = ["-date_created"]
  
class Exam(models.Model):
    """Exams"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="exams", null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    total_marks = models.IntegerField(default=0, null=True, blank=True)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    cohort = models.ForeignKey(StudentCohort, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='exam_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='exam_updated_by', null=True, blank=True, on_delete=models.SET_NULL)
    lecturer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lecturer_exam",
    )
    def __str__(self):
        return self.title

    objects = CourseMaterialManager()
   
    class Meta:
        ordering = ["-date_created"]

# schedule
class Schedule(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='schedule_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='schedule_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    def clean(self):
        # Exclude the current instance if it exists to avoid self-overlap during updates
        if self.pk:
            overlapping_schedules = Schedule.objects.filter(
                staff=self.staff,
                day=self.day,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)
        else:
            overlapping_schedules = Schedule.objects.filter(
                staff=self.staff,
                day=self.day,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )

        if overlapping_schedules.exists():
            raise ValidationError(f'Schedule conflict for {self.staff} on {self.day} between {self.start_time} and {self.end_time}.')

    def __str__(self):
        return f"{self.staff}, {self.course} {self.day} {self.start_time} - {self.end_time}"

# department
        
class Department(models.Model):
    """Department"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='department_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='department_updated_by', null=True, blank=True, on_delete=models.SET_NULL)
    head  = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="department_coordinator",
    )
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Program(models.Model):
    """Program"""
    name = models.CharField(max_length=200, unique=True)
    year_of_study = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='program_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='program_updated_by', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

# course registration period 
    
class CourseRegistrationPeriod(models.Model):
    """Course Registration Period"""
    STATUS_CHOICES = [
        (True, 'Open'),
        (False, 'Close')
    ]
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.BooleanField(default=False, choices=STATUS_CHOICES)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='course_registration_period_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='course_registration_period_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.academic_session} {self.academic_semester} Course Registration Period"
    
# calendar event
class CalendarEvent(models.Model):
    EVENT_TYPES = (
        ('important_date', 'Important Dates and Deadlines'),
        ('holiday', 'Holidays and Breaks'),
        ('academic_event', 'Academic Events'),
        ('social_event', 'Social Events'),
        ('other_event', 'Other Events'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='classroom_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='classroom_updated_by', null=True, blank=True, on_delete=models.SET_NULL)
    

    def __str__(self):
        return self.name

class ClassroomReservation(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='classroom_reservation_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='classroom_reservation_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.classroom.name} reserved by {self.user.username} from {self.start_time} to {self.end_time}"
    
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='equipment_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='equipment_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class EquipmentCheckout(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='equipment_checkout_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='equipment_checkout_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.equipment.name} checked out by {self.user.username} on {self.checkout_date}"
    
# announcement
class Announcement(models.Model):
    RECIPIENT_CHOICES = [
        ('students', 'Students'),
        ('faculty', 'Faculty'),
        ('institution', 'Institution')
    ]
    recipient = models.CharField(max_length=20, choices=RECIPIENT_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    file = models.FileField(upload_to="announcements", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='announcement_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='announcement_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.get_recipient_display()} - {self.title}"

class AdminAlert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('deadlines', 'Important Deadlines'),
        ('policy-updates', 'Policy Updates'),
        ('emergency-notifications', 'Emergency Notifications')
    ]
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    file = models.FileField(upload_to="admin_alerts", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='admin_alert_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='admin_alert_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.title}"





