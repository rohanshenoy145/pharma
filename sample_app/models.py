# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Medication(models.Model):
    medicationName = models.CharField(max_length = 100)
    dosageAmount = models.FloatField()
    dosageUnit = models.CharField(max_length = 100)
    dosageFrequency = models.IntegerField()