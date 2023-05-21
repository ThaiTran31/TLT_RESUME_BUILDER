from django.urls import path

from professional_summary import views

urlpatterns = [
    path('', views.Suggestions.as_view(),
         name='professional-summary-suggestions')
]
