from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
import pycountry


class Staff(models.Model):

    STATUS = [("active", "Active"), ("inactive", "Inactive")]

    GENDER = [("male", "Male"), ("female", "Female")]

    ROLE = [ ("admin", "Admin"), ("academic", "Academic")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    date_of_employment = models.DateField(default=timezone.now)
    role = models.CharField(max_length=10, choices=ROLE, default="academic")
    country = models.CharField( max_length=200, choices=[(country.name, country.name) for country in pycountry.countries], default="Gambia")
    image = models.ImageField(upload_to="staffs/images/", blank=True)
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name}"

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})
    

@receiver(post_save, sender=Staff)
def create_user_for_staff(sender, instance, created, **kwargs):
    if created and not instance.user:
        username = instance.firstname + instance.surname  # You can use the mat_number as the username
        password = "staff@utg"  # Generate a random password

        user = User.objects.create_user(username=username, password=password, is_staff=True)
        instance.user = user
        instance.save()


    