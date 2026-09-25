from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r"^[0-9+()\-\s]{7,20}$",
    message="Enter a valid phone number.",
)


class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
        OTHER = "Other", "Other"

    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    gender = models.CharField(max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField()
    address = models.TextField()
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.PROTECT,
        related_name="employees",
    )
    designation = models.CharField(max_length=150)
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    joining_date = models.DateField()
    profile_photo = models.ImageField(
        upload_to="employee_photos/",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

# Create your models here.
