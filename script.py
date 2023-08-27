"""
Iterate over all rows and map companies to recruiters

For each company, find the valid email format by trying first.last@company.com, flast@company.com, firstlast@company.com, etc
for the first recruiter. If the email fails to get sent for a format, try the next format. If the email is sent successfully, send the email to all recruiters in the company.
"""
import csv
from collections import defaultdict


def get_company_to_recruiters():
    with open("test.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    company_to_recruiters = defaultdict(list)
    for i in range(1, len(rows)):
        first_name = rows[i][0].lower().strip()
        last_name = rows[i][1].lower().strip()
        company = rows[i][2].lower().strip()
        company_to_recruiters[company].append((first_name, last_name))
    return company_to_recruiters


def get_company_to_email_format():
    company_to_email_format = dict()
    with open("formats.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        for r in rows:
            company_to_email_format[r[0].lower().strip()] = r[1].lower().strip()
    return company_to_email_format


# print(get_company_to_email_format())

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

    message = MIMEMultipart()
    message["From"] = sender_email
    to_email = template.format(first=first_name, last=last_name, company=company)
    print(to_email)
    message["To"] = "kirondeb02@gmail.com"
    message["Subject"] = "test subject"
    message.attach(MIMEText("test body", "plain"))

    attach_pdf_to_message(message, "Kiron_Deb_Resume.pdf")
    attach_pdf_to_message(message, "Recommendations.pdf")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            # server.sendmail(sender_email, to_email, message.as_string())
            server.sendmail(sender_email, "kirondeb02@gmail.com", message.as_string())
            response_code = server.quit()
            print(response_code)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}")
        print("Error:", e)


def email_recruiters(company_to_recruiters, company_to_email_format):
    company_to_recruiters = get_company_to_recruiters()
    print(company_to_recruiters)
    for company in company_to_recruiters:
        print(company)
        email_format = company_to_email_format[company]
        recruiters = company_to_recruiters[company]
        print(company, recruiters, email_format)
        for recruiter in recruiters:
            first_name, last_name = recruiter
            send_email(first_name, last_name, company, email_format)


# Read in csv
company_to_recruiters = get_company_to_recruiters()
company_to_email_format = get_company_to_email_format()
email_recruiters(company_to_recruiters, company_to_email_format)
