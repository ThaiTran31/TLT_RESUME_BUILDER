from django.urls import path

from resume_form import views

urlpatterns = [
    path("<int:pk>/delete-complex-section", views.ComplexSectionDelete.as_view(), name="complex-section-delete"),
    path("<int:pk>/delete-employment-history", views.EmploymentHistoryDelete.as_view(), name="employment-history-delete"),
    path("<int:pk>/delete-education", views.EducationDelete.as_view(), name="education-delete"),
    path("<int:pk>/delete-skill", views.SkillDelete.as_view(), name="skill-delete"),
    path("<int:pk>/delete-link", views.LinkDelete.as_view(), name="link-delete"),
    path("<int:pk>/delete-custom", views.CustomDelete.as_view(), name="custom-delete"),
    # path("<int:pk>/", views.ComplexSectionDetail.as_view(), name="complex-section-detail"),
    # path("<int:pk>/update", views.ComplexSectionUpdate.as_view()),
    # path("create/", views.ComplexSectionCreate.as_view()),
]
