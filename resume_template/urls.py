from django.urls import path, re_path

from . import views

# /products/
urlpatterns = [
    path('mock/', views.MockResumeTemplate.as_view()),
    path('', views.ResumeTemplateListAll.as_view(), name='resume_template_list_all'),
]
