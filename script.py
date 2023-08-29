import csv
from collections import defaultdict


def get_company_to_recruiters():
    with open("recruiters.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    company_to_recruiters = defaultdict(list)
    for i in range(1, len(rows)):
        name = rows[i][0].strip()
        company = rows[i][1].lower().strip()
        company_to_recruiters[company].append(name)
    return company_to_recruiters


def get_company_to_email_format():
    company_to_email_format = dict()
    with open("formats.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        for r in rows:
            company_to_email_format[r[0].lower().strip()] = r[1].lower().strip()
    return company_to_email_format


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()


def attach_pdf_to_message(message, pdf_filename):
    attachment = open(pdf_filename, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {pdf_filename}")
    message.attach(part)


def send_email(first_name, last_name, company, template):
    sender_email = os.getenv("GMAIL_ADDRESS")
    sender_password = os.getenv("GMAIL_PASSWORD")
    to_email = template.format(first=first_name, last=last_name, company=company)
    # to_email = "kirondeb02@gmail.com"
    subject = "Junior With 4 Prior SWE Internships"
    body = f"""
        Hi {first_name.capitalize()}!
        <br><br>
        I'm Kiron, a junior studying computer science at Johns Hopkins University. I'm interested in the Software Engineering Intern role at {company.capitalize()}.
        I have 10+ months of full-time software engineering experience, have received highly favorable LinkedIn recommendations from my managers at my two most 
        recent internships, and got a 600/600 on the <a href="https://app.codesignal.com/evaluation-result/h6e5RxPPmW8XSr62v?accessToken=DbEuGSiPvv38cEqNF-m6eknvzG2pfynLyeQ8FbYwoz">Codesignal General Coding Framework test</a>.<br>
        <br>
        I'm eager to advance my career at {company.capitalize()} and would love if you could take a look at my resume. I apologize if this email was intrusive - thank you so much for your time!
        <br>
        <br>
        Best,<br>
        Kiron<br>
        <a href="https://www.linkedin.com/in/kirondeb/">LinkedIn</a>
        """
    resume_filename = "Kiron_Deb_Resume.pdf"
    recommendations_filename = "Recommendations.pdf"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    attach_pdf_to_message(message, resume_filename)
    attach_pdf_to_message(message, recommendations_filename)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
            # server.sendmail(sender_email, "kirondeb02@gmail.com", message.as_string())
            response_code = server.quit()
            print(response_code)
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}")
        print("Error:", e)
        return False


def get_recruiters_emailed_already():
    with open("emailed_already.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    recruiters_emailed = set()
    for i in range(1, len(rows)):
        recruiters_emailed.add(rows[i][0].strip())
    return recruiters_emailed


def email_recruiters(company_to_recruiters, company_to_email_format):
    company_to_recruiters = get_company_to_recruiters()
    recruiters_emailed_already = get_recruiters_emailed_already()
    for company in company_to_recruiters:
        email_format = company_to_email_format[company]
        recruiters = company_to_recruiters[company]
        for recruiter in recruiters:
            if recruiter not in recruiters_emailed_already:
                first_name, last_name = recruiter.split(" ")
                if send_email(
                    first_name.lower(), last_name.lower(), company, email_format
                ):
                    with open("emailed_already.csv", "a") as f:
                        writer = csv.writer(f)
                        writer.writerow([recruiter])


# Read in csv
company_to_recruiters = get_company_to_recruiters()
company_to_email_format = get_company_to_email_format()
email_recruiters(company_to_recruiters, company_to_email_format)
