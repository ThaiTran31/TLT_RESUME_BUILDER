"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "TLT Resume Builder Administration"
admin.site.site_title = "TLT Resume Builder"
admin.site.index_title = "From TLT with Love"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("resume-form/", include("resume_form.urls")),
    path("resume/", include("resume.urls")),
    path("accounts/", include("accounts.urls")),
    path("resume-template/", include("resume_template.urls")),
    path("professional_summary/", include("professional_summary.urls")),
    path("jobs/", include("jobs.urls")),
    path("parse-resume/", include("parse_resume.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
