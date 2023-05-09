from django.urls import path

from resume import views

urlpatterns = [
    path('', views.ResumeList.as_view(), name='resume-list'),
    path("<int:pk>/", views.ResumeDetail.as_view(), name="resume-detail"),
    path("create/", views.ResumeCreate.as_view(), name="resume-create"),
    path("<int:pk>/delete/", views.ResumeDelete.as_view(), name="resume-delete"),
    path("update/", views.ResumeUpdate.as_view(), name="resume-update"),
    path("<int:pk>/duplicate/", views.ResumeDuplicate.as_view(), name="resume-duplicate"),
    path("<int:pk>/images-uploading/", views.ResumeImagesUploading.as_view(), name="images-uploading"),
]
