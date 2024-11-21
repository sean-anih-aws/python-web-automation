from selenium import webdriver
from twilio.rest import Client
from dotenv import load_dotenv
import os
import yagmail

# Load environment variables from .env file
load_dotenv()


def get_driver():
    # set options for driver to make scraping easier
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options)
    # fetch data from endpoint
    driver.get("https://katalon-demo-cura.herokuapp.com/")
    return driver


def send_email(details_obj):
    sender = os.getenv("FROM_EMAIL")
    receiver = os.getenv("TO_EMAIL")

    subject = "Cura Healthcare Appointment"

    content = f"""
    Cura Healthcare Appointment Confirmation Details:
    location: {details_obj['facility']}
    readmission: {details_obj['readmission']}
    program: {details_obj['program']}
    date: {details_obj['visit_date']}
    comments: {details_obj['comment']}
    """
    # get env variable
    gmail_app_pw = os.getenv("APP_PW")
    yag = yagmail.SMTP(user=sender, password=gmail_app_pw)

    # send multiple emails over a period of time
    yag.send(to=receiver, subject=subject, contents=content)
    print("sent confirmation email")


def send_text(details_obj):
    # Twilio credentials
    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    content = f"""
    Cura Healthcare Appointment Confirmation Details:
    location: {details_obj['facility']}
    readmission: {details_obj['readmission']}
    program: {details_obj['program']}
    date: {details_obj['visit_date']}
    comments: {details_obj['comment']}
    """

    message = client.messages.create(
        from_="+18336973859", body=content, to="+18777804236"
    )

    print("Message sent after booking:\n", message.sid)
