# Web Automation Project

## Overview

This project automates the process of booking an appointment on the Cura Healthcare demo site and provides confirmation notifications via email and SMS. It combines dynamic web scraping with notification systems to streamline appointment scheduling and enhance user experience.

## Core Features

### 1. **Web Scraping and Automation**

- Utilizes Selenium to navigate and interact with the [Cura Healthcare demo site](https://katalon-demo-cura.herokuapp.com/).
- Automates login, form selection, and submission for booking an appointment.
- Extracts appointment confirmation details from the site after successful booking.

### 2. **Notification System**

- **Email Notifications**: Sends appointment confirmation details to the user's email using `yagmail`. Email credentials and configuration are securely loaded via environment variables.
- **SMS Notifications**: Sends appointment confirmation details to the user's phone using Twilio's API. Twilio credentials are managed securely through environment variables.

### 3. **Reusable Helper Functions**

```
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
```

- **Driver Setup**: Configures the Selenium Chrome WebDriver for efficient scraping and automation (`get_driver()` function).
- **Email Sending**: Sends formatted appointment details via email (`send_email()` function).
- **SMS Sending**: Sends formatted appointment details via SMS (`send_text()` function).

## Workflow

```
from helpers import get_driver, send_text, send_email
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def main():
    # user input data
    appt_date = input("Enter appointment date in MM/DD/YYYY format: ")
    appt_comments = input("Add comments for the doctor: ")

    # navigate to login page and log in
    driver = get_driver()
    driver.find_element(by="id", value="btn-make-appointment").click()
    driver.find_element(by="id", value="txt-username").send_keys("John Doe")
    driver.find_element(by="id", value="txt-password").send_keys(
        "ThisIsNotAPassword" + Keys.RETURN
    )

    # Locate the dropdown element and select option
    dropdown = driver.find_element(
        by="xpath", value="/html/body/section/div/div/form/div[1]/div/select"
    )
    select = Select(dropdown)
    select.select_by_value("Hongkong CURA Healthcare Center")

    # checkbox and radio button
    driver.find_element(by="id", value="chk_hospotal_readmission").click()
    driver.find_element(by="id", value="radio_program_none").click()

    # enter appointment date
    driver.find_element(by="id", value="txt_visit_date").send_keys(appt_date)

    # add comments
    driver.find_element(by="id", value="txt_comment").send_keys(appt_comments)

    # book appointment and get confirmation details
    driver.find_element(
        by="xpath", value="/html/body/section/div/div/form/div[6]/div/button"
    ).click()

    confirmation_details = {
        "facility": driver.find_element(by="id", value="facility").text,
        "readmission": driver.find_element(by="id", value="hospital_readmission").text,
        "program": driver.find_element(by="id", value="program").text,
        "visit_date": driver.find_element(by="id", value="visit_date").text,
        "comment": driver.find_element(by="id", value="comment").text,
    }

    # send confirmation email/text
    send_email(confirmation_details)
    send_text(confirmation_details)


if __name__ == "__main__":
    main()
```

1. **User Input**:
   - Prompts the user to enter the appointment date and comments for the doctor.
2. **Booking Process**:

   - Logs into the demo site with pre-defined credentials.
   - Interacts with the booking form to select a healthcare facility, specify options, and input the appointment date and comments.
   - Submits the form and retrieves confirmation details.

3. **Confirmation and Notifications**:
   - Formats the extracted confirmation details.
   - Sends the confirmation details to the user via both email and SMS.

## Technologies Used

- **Selenium**: For web automation and interaction.
- **Twilio**: For sending SMS notifications.
- **Yagmail**: For sending email notifications.
- **Python-dotenv**: For securely managing environment variables.

## Highlights

- **Dynamic Web Automation**: Fully automates interaction with the demo site, including navigation, form filling, and data extraction.
- **Multi-Channel Notifications**: Delivers appointment confirmation details via both email and SMS for convenience.
- **Secure Configuration**: Uses environment variables to manage sensitive information like credentials and API keys.
- **Modular Design**: Helper functions improve code reusability and maintainability.

This project demonstrates a practical integration of web scraping and notification systems for automated appointment scheduling and confirmation delivery.
