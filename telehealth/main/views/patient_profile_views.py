from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import render, redirect, reverse
from .mixins import LoginProhibitedMixin
from ..forms import *


class ShowPatientProfileView(LoginRequiredMixin, DetailView):
    pass

