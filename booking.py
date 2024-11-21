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
