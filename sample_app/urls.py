# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import admin
from django.urls import path, re_path
from sample_app import views

urlpatterns = [

    # Matches any html file
    path("admin/", admin.site.urls),
    path("",views.homeAction,name = "homeAction"),
    path("submitMed/",views.submitMed,name = "submit_medication")
    

]
