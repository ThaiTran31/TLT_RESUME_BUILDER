from django.urls import path

from jobs import views

urlpatterns = [
    path("searching/", views.JobSearchingAPIView.as_view(), name="job-searching"),
    path("", views.JobPostingListAPIView.as_view(), name="job-list-all"),
]
