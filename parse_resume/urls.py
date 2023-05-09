from django.urls import path

from parse_resume import views

urlpatterns = [
    path('', views.ParseResume.as_view(),
         name='resume-parser')
]
