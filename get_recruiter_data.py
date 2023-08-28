import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()

pattern = r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"


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
    print(results)
    return results


import csv

companies = {"stripe", "google", "databricks", "amazon", "microsoft", "meta"}
for company in companies:
    recruiters = get_university_recruiters(company)
    for recruiter in recruiters:
        # Add to recruiters.csv using csv module
        with open("recruiters.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([recruiter, company])
