
import undetected_chromedriver as uc
import random
from driverActions import DriverActions
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import random
from smsactivate.api import SMSActivateAPI
import re
import imaplib
import email
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import sys

def get_emails(username, password, _from):
    gmail_host= 'imap.gmx.net'
    #set connection
    mail = imaplib.IMAP4_SSL(gmail_host)
    #login
    mail.login(username, password)
    #select inbox
    mail.select("INBOX")
    #select specific mails
    _, selected_mails = mail.search(None, f'(FROM "{_from}")')
    #total number of mails from specific user
    total_mails = len(selected_mails[0].split())
    # print("Total Messages from noreply@kaggle.com:" , total_mails)
    all_emails = []
    for num in selected_mails[0].split():
        _email = {}
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]
        #convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)
        #access data
        _email["subject"] = email_message["subject"]
        _email['to'] =  email_message["to"]
        _email['from'] = email_message["from"]
        _email['date'] = email_message["date"]
        _email['message'] = ''
        for part in email_message.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                _email['message'] += message.decode()
                break
        all_emails.append(_email)
    return all_emails

def get_random_name():
    with open('names.json') as file:
        names = json.load(file)
    first, last = random.choice(names), random.choice(names)
    return first, last

def get_email_account():
    with open('email_accounts.txt', 'r') as file:
        emails = file.readlines()
        email = emails[0]
    with open('email_accounts.txt', 'w', newline="") as file:
        file.writelines("".join(emails[1:])) 
    return email.strip()

def get_code(id):
    while True:
        msg = sa.getFullSms(id) #'STATUS_WAIT_CODE'
        print(msg)
        if msg == 'STATUS_WAIT_CODE':
            sleep(10)
            continue
        return msg    


SMSACTIVATE_KEY = "3987f73e5cc536319d13d03c02ee734B"


sa = SMSActivateAPI(SMSACTIVATE_KEY)
sa.debug_mode = True # Optional action. Required for debugging


n_accounts = int(input("How many accounts? "))
created = 0


while created < n_accounts:
    try:
        fname, lname = get_random_name()
        country = "GB"
        dob_day = random.randint(1, 28)
        dob_month = random.randint(1, 12)
        dob_year = random.randint(1980, 2002)
        gender = random.choice(['MALE', "FEMALE"])
        password = "snwiho21@@ns"
        try:
            email_acc = get_email_account()
        except:
            sys.exit("Out of email accounts")
        # email_acc = "xagin54757@vasqa.com:xagin54757@vasqa.com"
        email_address, email_password = email_acc.split(':')

        country = country.lower()
        country_full = "United Kingdom"
        city = "London"
        postal_code = "EC1A"
        recent_job_title = 'Supervisor'
        recent_company = "ranchers"

        # chrome_options = uc.ChromeOptions()
        # chrome_options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        # driver = uc.Chrome(options=chrome_options)
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        driver_actions = DriverActions(driver)
        driver.get('https://www.linkedin.com/signup')
        while True:
            driver_actions.send_keys('//*[@id="email-address"]', email_address)
            driver_actions.send_keys('//*[@id="password"]', email_password)
            if driver_actions.get_el('//*[@id="email-address"]').get_attribute('value'): break

        driver_actions.click('//button[@type="submit"]')
        driver_actions.send_keys('//*[@id="first-name"]', fname)
        driver_actions.send_keys('//*[@id="last-name"]', lname)

        driver_actions.click('//button[@type="submit"]')
        verf_frame = driver_actions.get_el('//iframe[@title="Security verification"]')
        driver.switch_to.frame(verf_frame)
        while True:
            driver_actions.select_by_value('//select[@name="countryCode"]', country)
            phone_id, phone = sa.getNumber('tn', country=16).values()
            phone_number = str(phone)
            driver_actions.send_keys('//*[@id="register-verification-phone-number"]', phone_number)
            driver_actions.click('//button[@type="submit"]')
            try:
                driver_actions.get_el('//span[@role="alert" and contains(text(), "use this phone number")] ', wait=5)
                continue
            except:
                pass
                
            sa.setStatus(status=1, id=phone_id)
            break

        otp = get_code(phone_id)
        otp = re.findall('\d+', otp)[0]
        driver_actions.send_keys('//input[@name="pin"]', otp)
        driver_actions.click('//button[@type="submit"]')


        sleep(2)
        while True:
            try:
                driver_actions.send_keys('//input[@id="typeahead-input-for-country"]', country_full)
                sleep(1.5)
                driver_actions.click(f'//span[contains(@class,"search-typeahead") and text()="{country_full}"]')
                driver_actions.send_keys('//input[@id="typeahead-input-for-postal-code"]', postal_code)

                driver_actions.click('//button')
                break
            except:
                continue
        while True:
            try:
                driver_actions.send_keys('//input[@id="typeahead-input-for-title"]', recent_job_title)
                sleep(1.5)
                driver_actions.click('//span[contains(@class,"search-typeahead")]')
                employment_type = "urn:li:fsd_employmentType:12"
                driver_actions.select_by_value('//select[@id="typeahead-input-for-employment-type-picker"]', employment_type)
                break
            except:
                continue

        while True:
            try:
                driver_actions.send_keys('//input[@id="typeahead-input-for-company"]', recent_company)
                sleep(1.5)
                driver_actions.click('//span[contains(@class,"search-typeahead")]')

                driver_actions.click('//span[text()="Continue"]//parent::button')
                break
            except:
                continue
        _email = get_emails(email_address, email_password, 'security-noreply@linkedin.com')[-1]
        email_otp = re.findall('\d+' ,_email['message'])[0]
        email_otp = re.findall('\d+', email_otp)[0]
        # email_otp = '006250'
        # driver.close()
        # driver.switch_to.window(driver.window_handles[-1])
        # 

        driver_actions.send_keys('//input[@id="email-confirmation-input"]', email_otp)
        driver_actions.click('//span[text()="Agree & Confirm"]//parent::button')
        # driver_actions.click('//span[text()="Not now"]//parent::button')
        # driver_actions.send_keys('//input[@id="typeahead-input-for-country"]', country_full)
        # driver_actions.click(f'//span[contains(@class,"search-typeahead") and text()="{country_full}"]')
        # driver_actions.send_keys('//input[@id="typeahead-input-for-postal-code"]', postal_code)

        # driver_actions.click('//button')
        driver_actions.click('//span[text()="Not now"]//parent::button') #< sometimes dosen't occur
        driver_actions.click('//span[text()="Skip"]//parent::button')
        current_url  = driver.current_url
        driver_actions.click('//button[text()="Skip"]')
        # driver_actions.send_keys('//input[@role="combobox"]', 'shoaibatiq')

        WebDriverWait(driver, 5).until(lambda x: driver.current_url != current_url)
        current_url  = driver.current_url
        driver_actions.click('//span[text()="Skip"]//parent::button')
        # WebDriverWait(driver, 5).until(lambda x: driver.current_url != current_url)

        # driver_actions.click('//span[text()="Skip"]//parent::button') #<add dp>
        print('here')
        driver_actions.click('//span[text()="Next"]//parent::button')
        print('here2')

        els = driver.find_elements('xpath', '//span[text()="Follow"]//parent::button')
        try:
            for i in range(5):
                # driver.execute_script("arguments[0].scrollIntoView();", els[i])
                driver.execute_script("arguments[0].click();", els[i])

                sleep(0.3)
        except: pass
        driver_actions.click('//span[text()="Finish"]//parent::button')

        sleep(2)
        driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(1)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        els = driver.find_elements('xpath', '//span[text()="Connect"]//parent::button')

        for i in range(10%len(els)):
            driver.execute_script("arguments[0].click();", els[i])

        driver.get('https://www.linkedin.com/in/')

        driver_actions.js_click('//main//span[text()="Add profile section"]//parent::button')
        # get_emails(email_address+'@gmx.com', password, 'shoaibatiq405@gmail.com')
        driver_actions.click('//span[text()="Add about"]//parent::a')
        driver_actions.send_keys('//textarea', 'hello world')
        driver_actions.click('//span[text()="Save"]//parent::button')

        # driver.get('https://www.linkedin.com/in/')
        # driver_actions.js_click('//button[@aria-label="Edit photo"]')
        # driver_actions.send_keys('//input[@accept="image/*"]', 'C:/Users/shoai/Documents/py/linkedin-account-creator/images.png')
        # driver_actions.click('//span[text()="Save photo"]//parent::button')
        with open('accounts.txt', 'a') as file:
            file.writelines([f"{email_address}:{password}\n"])
        created += 1
    except Exception as e: print(e)





