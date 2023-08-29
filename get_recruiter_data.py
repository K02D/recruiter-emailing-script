import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()

pattern = r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"


def get_recruiters_added_already():
    with open("recruiters.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    recruiters_emailed = set()
    for i in range(1, len(rows)):
        recruiters_emailed.add(rows[i][0].strip())
    return recruiters_emailed


def get_university_recruiters(company):
    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {
        "cx": "a4cc2c236a1b740ff",
        "key": os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY"),
        "q": f"site:linkedin.com university recruiter at {company}",
        "start": "1",
    }
    headers = {"Accept": "application/json"}
    results = []
    for _ in range(5):
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        search_results = data["items"]
        for s in search_results:
            full_name = re.findall(pattern, s["title"])
            if len(full_name) > 0:
                results.append(full_name[0])
        params["start"] = data["queries"]["nextPage"][0]["startIndex"]
    return results


import csv

companies = {
    "stripe",
    "google",
    "databricks",
    "amazon",
    "microsoft",
    "meta",
    "atlassian",
    "linkedin",
}

recruiters_added_already = get_recruiters_added_already()

for company in companies:
    recruiters = get_university_recruiters(company)
    print(f"Getting recruiters for {company}")
    for recruiter in recruiters:
        if recruiter not in recruiters_added_already:
            print(f"Adding {recruiter}")
            with open("recruiters.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow([recruiter, company])
