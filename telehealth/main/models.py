from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_managers import UserManager
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    """Username is user's email"""
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)

    first_name = models.CharField(max_length=50, unique=False, blank=False, null=False)
    last_name = models.CharField(max_length=50, unique=False, blank=False, null=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def is_patient(self):
        return Patient.objects.filter(email=self.email).exists()

    def is_doctor(self):
        return Doctor.objects.filter(email=self.email).exists()


class Patient(User):

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Doctor(User):
    single_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="doctors_of_this_patient")

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

