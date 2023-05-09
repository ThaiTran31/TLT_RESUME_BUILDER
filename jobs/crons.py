from .scrapers import LinkedinScraper, VNWorksScraper
from .models import JobPosting
from .documents import JobPostingDocument

JOB_TITLES = [
    'Software Developer',
    # 'Sales Officer',
    # 'Accountant',
]

LOCATIONS = [
    'Ho Chi Minh city, Vietnam',
    # 'Da Nang city, Vietnam',
    # 'Ha Noi city, Vietnam'
]


def job_postings_scraping_cron_job():
    JobPosting.objects.all().delete()
    for job_title in JOB_TITLES:
        for location in LOCATIONS:
            vnw_jobs = VNWorksScraper(job_title, location)
            JobPostingDocument().update(vnw_jobs)
            lin_jobs = LinkedinScraper(job_title, location)
            JobPostingDocument().update(lin_jobs)
