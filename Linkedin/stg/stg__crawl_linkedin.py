
# Import libraries
import requests
import time
from bs4 import BeautifulSoup
import random
import pandas as pd

url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}
job_searchs = ["data analyst","data engineer","machine learning","artificial intelligence","business intelligence"]
job_searchs = ["business intelligence"]
location = "Vietnam"
max_load = 250

def get_company_size(company_url):
    try:
        r = requests.get(company_url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        size_tag = soup.find("span",string=lambda x: x and "employees" in x.lower())
        return size_tag.text.strip() if size_tag else None
    except Exception as e:
        print(f"Company size error: {company_url}")
        return None

def get_job_detail(job_url):
    try:
        r = requests.get(job_url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        desc_div = soup.find("div", class_="show-more-less-html__markup")
        if desc_div:
            return desc_div.get_text(" ", strip=True)
        return None
    except Exception as e:
        print(f"JD error: {job_url} - {e}")
        return None
def clean_keyword(keyword):
    return keyword.lower().replace(" ","_")

for keyword in job_searchs:
    print(f"\nSearching keyword: {keyword}")
    all_jobs = []
    for start in range(0, max_load, 25):
        print(f"  start={start}")
        params = {
            "keywords": keyword,
            "location": location,
            "start": start
        }

        response = requests.get(url, headers=headers, params=params, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all("li")
        print(f"   → found {len(cards)} jobs")

        if not cards:
            break

        for card in cards:
            #  extract job_id
            # base_card_div = card.find("div", {"class": "base-card"})
            # job_id = base_card_div.get("data-entity-urn").split(":")[3]

            #  extract job_title, company name and location
            title = card.find("h3")
            company = card.find("h4")
            # company_link_tag = company.find("a",class_ = "hidden-nested-link")
            # company_url = company_link_tag["href"] if company_link_tag else None
            location = card.find("span", class_="job-search-card__location")

            # extract url
            link = card.find("a", href=True)
            job_url = link["href"] if link else None

            # extract description
            job_description = get_job_detail(job_url)
            # company_size = get_company_size((company_url))

            # extract posted date and number of applicants
            posted = card.find("time")
            # num_applicants = card.find("span", {"class":"num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"})

            # append infor
            all_jobs.append({
                "keyword": keyword,
                # "job_id": job_id,
                "job_title": title.text.strip() if title else None,
                "company": company.text.strip() if company else None,
                "location": location.text.strip() if location else None,
                "posted_time": posted.text.strip() if posted else None,
                # "num_applicants": num_applicants.text.strip() if num_applicants else None,
                "job_url": link["href"] if link else None,
                "job_description": job_description
                # "company_size": company_size
            })
        time.sleep(2)
    keyword_clean = clean_keyword(keyword)
    file_name = f"linkedin_jobs_{keyword_clean}.csv"
    df = pd.DataFrame(all_jobs).drop_duplicates(subset=["job_url"])
    df.to_csv(file_name, index=False)
    time.sleep(5)

df_all = []
for kw in job_searchs:
    keyword_clean = clean_keyword(kw)
    file_name = f"linkedin_jobs_{keyword_clean}.csv"
    df = pd.read_csv(file_name)
    df_all.append(df)
merged_df = pd.concat(df_all,ignore_index = False)
merged_df.to_csv("linkedin_jobs.csv", index = False)
