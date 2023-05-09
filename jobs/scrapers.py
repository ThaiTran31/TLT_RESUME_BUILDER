from copy import deepcopy
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

from .models import JobPosting

LINKEDIN_JOB_POST_CLASSNAME = "base-card"
LINKEDIN_JOB_TITLE_CLASSNAME = "base-search-card__title"
LINKEDIN_COMPANY_CLASSNAME = "base-search-card__subtitle"
LINKEDIN_LOCATION_CLASSNAME = "job-search-card__location"
LINKEDIN_JOB_LINK_CLASSNAME = "base-card__full-link"
LINKEDIN_DATE_CLASSNAME = "job-search-card__listdate"
LINKEDIN_JOB_ID_CLASSNAME = "data-entity-urn"
LINKEDIN_JOB_DETAILS_WRAPPER = "show-more-less-html__markup"
LINKEDIN_TARGET_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_title}&location={location}&geoId=&f_TPR=r604800&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={starter}"
LINKEDIN_DEEPER_TARGET_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"


VNW_PAYLOAD_TEMPLATE = {
    "hitsPerPage": 50,
    "order": [],
    "ranges": [],
    "retrieveFields": [
        "alias",  # for constructing details link
        "jobId",  # for constructing details link
        "address",
        "jobTitle",
        "companyName",
        "expiredOn",
        "approvedOn",
        "jobDescription",
        "jobRequirement",
        "jobUrl"
    ]
}
VNW_TARGET_URL = "https://ms.vietnamworks.com/job-search/v1.0/search"
VNW_ENCODED_LOCATION = {
    "Ho Chi Minh city, Vietnam": "29",
    "Da Nang city, Vietnam": "17",
    "Ha Noi city, Vietnam": "24",
}


def LinkedinScraper(job_title, location):
    job_list = []
    job = {}
    page_num = 0
    while len(job_list) < 50:
        print(LINKEDIN_TARGET_URL.format(job_title=job_title, location=location, starter=page_num))
        print("------------------------------------------------------------------------------------")
        response = requests.get(LINKEDIN_TARGET_URL.format(job_title=job_title, location=location, starter=page_num))
        soup = BeautifulSoup(response.content, "html.parser")
        all_jobs_on_this_page = soup.find_all("li")
        if len(all_jobs_on_this_page) > 0:
            for post in all_jobs_on_this_page:
                job_ele = post.find("div", {"class": LINKEDIN_JOB_POST_CLASSNAME})
                try:
                    job["title"] = job_ele.find("h3", {"class": LINKEDIN_JOB_TITLE_CLASSNAME}).text.strip()
                except Exception:
                    continue
                try:
                    job["company"] = job_ele.find("h4", {"class": LINKEDIN_COMPANY_CLASSNAME}).text.strip()
                except Exception:
                    continue
                try:
                    job["location"] = job_ele.find("span", {"class": LINKEDIN_LOCATION_CLASSNAME}).text.strip()
                except Exception:
                    continue
                try:
                    job["link"] = job_ele.find("a", {"class": LINKEDIN_JOB_LINK_CLASSNAME})["href"]
                except Exception:
                    continue
                try:
                    time_ago = job_ele.find("time", {"class": LINKEDIN_DATE_CLASSNAME}).text.strip()
                    if 'hour' in time_ago:
                        job["date"] = date.today()
                    else:
                        days_delta = time_ago.split()[0]
                        job["date"] = date.today() - timedelta(days=int(days_delta))
                except Exception:
                    continue
                # scrape job details from job id
                job_id = job_ele.get(LINKEDIN_JOB_ID_CLASSNAME).split(":")[3]
                deeper_response = requests.get(LINKEDIN_DEEPER_TARGET_URL.format(job_id=job_id))
                deeper_soup = BeautifulSoup(deeper_response.content, "html.parser")
                try:
                    wrapper = deeper_soup.find("div", {"class": LINKEDIN_JOB_DETAILS_WRAPPER})
                    details_list = wrapper.find_all("li")
                    acc_details = ""
                    for details in details_list:
                        acc_details += '#' + details.text.strip()
                    job["details"] = acc_details
                except Exception:
                    continue
                job_list.append(JobPosting(
                    job_portal="linkedin",
                    job_title=job["title"],
                    company=job["company"],
                    date=job["date"],
                    link=job["link"],
                    location=job["location"],
                    details=job["details"],
                    searching_location=location
                ))
                job = {}
        else:
            break
        page_num += len(all_jobs_on_this_page)
    return JobPosting.objects.bulk_create(job_list)


def VNWorksScraper(job_title, location):
    job_list = []
    page_num = 0
    payload = deepcopy(VNW_PAYLOAD_TEMPLATE)
    config_filter = [
        {
            "field": "workingLocations.cityId",
            "value": VNW_ENCODED_LOCATION[location],
        },
        {
            "field": "workingLocations.districtId",
            "value": "[{{\"cityId\":{},\"districtId\":[-1]}}]".format(VNW_ENCODED_LOCATION[location])
        }
    ]
    payload["filter"] = config_filter
    payload["query"] = job_title
    while len(job_list) < 70:
        payload["page"] = page_num
        print(payload)
        print('-------------------------------------------------------------------------')
        response = requests.post(VNW_TARGET_URL, json=payload)
        data = response.json().get("data")
        print("the number of posting shot " + str(page_num) + ": " + str(len(data)))
        if len(data) > 0:
            for item in data:
                job_list.append(JobPosting(
                    job_portal="vietnamworks",
                    job_title=item["jobTitle"],
                    company=item["companyName"],
                    date=item["approvedOn"].split('T')[0],
                    link=item["jobUrl"],
                    location=item["address"],
                    details=item["jobDescription"] + '#' + item["jobRequirement"],
                    searching_location=location
                ))
        else:
            break
        page_num += 1
    return JobPosting.objects.bulk_create(job_list)
