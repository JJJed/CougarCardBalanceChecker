import requests
from email.message import EmailMessage
import ssl
import smtplib
import os


def get_balance(student_id, cafe_id):
    url = "https://thecougarcard.org/getTranscationHistory?student_id=" + str(student_id) + "&cafe_id=" + str(cafe_id)
    r = requests.post(url)
    text = r.text
    index = text.rfind("balance_amount")
    text = text[index + 16:]
    texts = text.split(",")
    text = texts[0]
    try:
        text = float(text)
    except ValueError:
        text = 0.00
    text = "%0.2f" % text
    text = "$" + text
    return text


def get_verified():
    file = open("verified.txt", "r")
    verified = file.readlines()
    file.close()
    for i in range(len(verified)):
        verified[i] = verified[i].replace("\n", "")
    return verified


def send_emails(name, email):
    local_address = "cougarcardbalance@jeddev.net"
    gmail_address = "cougarcardbalance@gmail.com"
    local_password = os.environ.get("EMAIL_PASSWORD")

    subject1 = "Verification Request Received"
    body1 = f'Hi {first_name(name)},\nYour cougar card balance ID verification request has been received. You will receive an update with your ID if your request is approved.'

    subject2 = "New Verification Request"
    body2 = f'New cougar card balance ID verification request.\nName: {name}\nEmail: {email}'

    em1 = EmailMessage()
    em1["From"] = local_address
    em1["To"] = email
    em1["Subject"] = subject1
    em1.set_content(body1)

    em2 = EmailMessage()
    em2["From"] = local_address
    em2["To"] = gmail_address
    em2["Subject"] = subject2
    em2.set_content(body2)

    context = ssl.create_default_context()

    with smtplib.SMTP("mail.jeddev.net", 587) as smtp:
        smtp.starttls(context=context)

        smtp.login(local_address, local_password)

        smtp.sendmail(local_address, email, em1.as_string())
        smtp.sendmail(local_address, gmail_address, em2.as_string())


def send_approval_email(user_id, email, name):
    local_address = "cougarcardbalance@jeddev.net"
    local_password = os.environ.get("EMAIL_PASSWORD")

    subject = "Verification Request Approved"
    body = f'Hi {first_name(name)},\nYour cougar card balance ID verification request has been approved. Your user ID is {user_id}.\nYou can check your balance at https://ccbal.jeddev.net'

    em = EmailMessage()
    em["From"] = local_address
    em["To"] = email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP("mail.jeddev.net", 587) as smtp:
        smtp.starttls(context=context)

        smtp.login(local_address, local_password)

        smtp.sendmail(local_address, email, em.as_string())


def first_name(name):
    return name.split()[0].capitalize()


def db_email():
    local_address = "cougarcardbalance@jeddev.net"
    local_password = os.environ.get("EMAIL_PASSWORD")

    email = "cougarcardbalance@gmail.com"

    subject = "DATABASE ERROR"
    body = """
DATABASE ERROR, RESTART APP ASAP
https://webhosting4000.is.cc:2222/evo/user/plugins/python_selector#/applications/domains%2Fccbal.jeddev.net%2Fpublic_html%2Fmyapp
"""

    em = EmailMessage()
    em["From"] = local_address
    em["To"] = email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP("mail.jeddev.net", 587) as smtp:
        smtp.starttls(context=context)

        smtp.login(local_address, local_password)

        smtp.sendmail(local_address, email, em.as_string())
