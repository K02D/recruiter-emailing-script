import requests
from bs4 import BeautifulSoup


def get_stripe_university_recruiters():
    url = "https://www.linkedin.com/jobs/search/?keywords=stripe%20university%20recruiter&location=Anywhere"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    recruiters = []
    print(response.content)
    for li in soup.find_all("li", class_="result-item"):
        recruiter = {}
        recruiter["name"] = li.find("h3", class_="result-title").text
        recruiter["linkedin_url"] = li.find("a", class_="result-link")["href"]
        recruiters.append(recruiter)

    return recruiters


recruiters = get_stripe_university_recruiters()
print(recruiters)
for recruiter in recruiters:
    print(recruiter["name"] + ": " + recruiter["linkedin_url"])
