from .scrapers import LinkedinScraper, VNWorksScraper
from .models import JobPosting, JobTitleSearchTerm, LocationSearchTerm
from .documents import JobPostingDocument


def job_postings_scraping_cron_job():
    JobPosting.objects.all().delete()
    job_title_list = JobTitleSearchTerm.objects.values_list("term", flat=True).distinct()
    location_list = LocationSearchTerm.objects.values_list("term", flat=True).distinct()
    for job_title in job_title_list:
        for location in location_list:
            vnw_jobs = VNWorksScraper(job_title, location)
            JobPostingDocument().update(vnw_jobs)
            lin_jobs = LinkedinScraper(job_title, location)
            JobPostingDocument().update(lin_jobs)
