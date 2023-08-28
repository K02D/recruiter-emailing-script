import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()

pattern = r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"


def get_stripe_university_recruiters():
    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {
        "cx": "a4cc2c236a1b740ff",
        "key": os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY"),
        "q": "site:linkedin.com university recruiter at stripe",
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


get_stripe_university_recruiters()
