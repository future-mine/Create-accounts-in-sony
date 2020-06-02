import csv
import zipfile
import time
import random
import string
import requests
import os.path
import threading
import imaplib
import getpass, os, imaplib, email
import tkinter as tk
import names
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from email.parser import HeaderParser
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import randint


def read_config_data():
    with open('city.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        global list_city
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if (line_count % 2) == 0:
                    line_count += 1
                    continue
                city = {}
                city['City Name'] = row[0]
                city['Postal Code'] = row[1]
                city['State'] = row[2]
                list_city.append(city)
                line_count += 1

                
        
        print(f'Processed {line_count} lines.')


# Create random Email
def Create_email():
    letters = string.ascii_lowercase
    email = ''.join(random.choice(letters) for i in range(randint(5,7)))
    for j in range(randint(4,7)):
        email += str(randint(0,9))
    email += "@liveemail24.de"
    return email

# Create agent list. as much as user inupt
def Create_agent_list(num_account):
    
    for i in range(num_account):
        index = randint(1,city_limit)
        amount_proxy = len(list_proxy)-1
        agent = {}
        agent['Email'] = Create_email()
        agent['City'] = list_city[index]['City Name']
        agent['Postal Code'] = list_city[index]['Postal Code']
        agent['State'] = list_city[index]['State']
        agent['First Name'] = names.get_first_name(gender='male')
        agent['Last Name'] = names.get_last_name()
        agent['Proxy Ip'] = list_proxy[randint(0,amount_proxy)]['IP']
        agent['Proxy Port'] = list_proxy[randint(0,amount_proxy)]['Port']
        agent['Email Pwd'] = ""
        list_agent.append(agent)

def read_proxy_data():
    with open('proxy.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        global list_proxy
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                proxy = {}
                proxy['IP'] = row[0]
                proxy['Port'] = row[1]
                list_proxy.append(proxy)
                line_count += 1
        print(f'Processed {line_count} lines.')

# Generate Password (should not involve continusly number or letter)
def generate_password(stringLength=10):
    letters = string.ascii_lowercase
    password =  ''
    for i in range(4):
        newnum = str(randint(0,9))
        newletter = random.choice(letters)
        password += newnum + newletter
    return password

# Create Chrome driver
def Create_normal_driver():

    # capabilities['proxy']['socksUsername'] = proxy['username']
    # capabilities['proxy']['socksPassword'] = proxy['password']
    options = Options()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=default')
    options.add_argument('--incognito')
    options.add_argument('--disable-plugin-discovery')
    options.add_argument('--start-maximized')
    options.add_argument("--enable-automation")
    options.add_argument("--test-type=browser")

    driver = webdriver.Chrome(executable_path="chromedriver", options = options)
    # desired_capabilities=capabilities
    time.sleep(3)
    
    return driver

def Create_driver(address = "23.88.195.47:23667", username = "mare", userpass = "WuBA8ujAD"):
    proxy = {'address': address,
            'username': username,
            'password': userpass}

    capabilities = dict(DesiredCapabilities.CHROME)
    capabilities['proxy'] = {'proxyType': 'MANUAL',
                            'httpProxy': proxy['address'],
                            'ftpProxy': proxy['address'],
                            'sslProxy': proxy['address'],
                            "noProxy":None,
                            "proxyType":"MANUAL",
                            "class":"org.openqa.selenium.Proxy",
                            "autodetect":False}


    # capabilities['proxy']['socksUsername'] = proxy['username']
    # capabilities['proxy']['socksPassword'] = proxy['password']

    options = Options()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=default')
    options.add_argument('--incognito')
    options.add_argument('--disable-plugin-discovery')
    options.add_argument('--start-maximized')
    options.add_argument("--enable-automation")
    options.add_argument("--test-type=browser")
    options.add_argument('--proxy-server=%s' %  proxy['address'])

    driver = webdriver.Chrome(executable_path="chromedriver", desired_capabilities=capabilities)
    # driver = webdriver.Chrome(executable_path="chromedriver", options = options)
    # desired_capabilities=capabilities
    time.sleep(3)
    print('return driver')
    upgrade_status(proxy['address'])
    
    return driver
# save account information
def save_all_data(Email = "", firstname = "", lastname = "",  password = "",  birth_day = "", online_id = "", email_pwd = "", proxy = "", status = "", Country = "", City = "",State = "", Postal_code = ""):
    upgrade_status("[:--->> Saving result data...")
    write_header = False
    if not os.path.exists('account.csv'):
        write_header = True
    with open('account.csv', 'a', newline='') as csvfile:

        fieldnames = ['Email','Password', 'Country','Language','Date of birth','City','State/Province','Postal Code','Online ID','First Name','Last Name','Email PW','Proxy','Result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow({'Email' : Email,'Password': password, 'Country': Country,'Language':"English",'Date of birth':birth_day,
                        'City': City,'State/Province': State ,'Postal Code': Postal_code,'Online ID' : online_id,'First Name' : firstname,'Last Name' : lastname,'Email PW' :email_pwd,'Proxy' : proxy, 'Result' : status})

# save log file
def export_logfile(data):
    with open("Log.txt","a") as f:
        f.write(" \n\n\n @@ : " + time.ctime())
        f.write("\n")
        f.write(data)
        f.write("\n")

def request(driver):  
    s = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
    print(s)
    return s

def pass_captcha (driver):
    API_KEY = '04d52e55eaff4ed7999e9636eb8d8839'
    site_key = '6Le-UyUUAAAAAIqgW-LsIp5Rn95m_0V0kt_q0Dl5'
                
    url = 'https://id.sonyentertainmentnetwork.com/create_account/'
    s = request(driver)

    captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(
        API_KEY, site_key, url)).text.split('|')[1]

    recaptcha_answer = s.get(
        "http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    upgrade_status("[:--->> solving ref captcha...")

    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        time.sleep(5)
        recaptcha_answer = s.get(
            "http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
        upgrade_status("[:--->> waiting token......")
    recaptcha_answer = recaptcha_answer.split('|')[1]
    upgrade_status(recaptcha_answer)

    return recaptcha_answer


def email_verify():

    driver = Create_normal_driver()
    try:
        conn = imaplib.IMAP4_SSL(host='ha01s015.org-dns.com')
        (retcode, capabilities) = conn.login("catchall_email","catchall_email_pw")
    
    except:
        return "Error Log in"
    init_amount = 0
    comming = False
    for i in range(20):
        # conn.select(readonly = 1)
        time.sleep(3)
        typ, mcount = conn.select("Inbox")
        (retcode, message) = conn.search(None,'(UNSEEN)')
        print(int(mcount[0]))
        print(message[0])
        mail_ids = []
        for block in message:
            mail_ids += block.split()
        if comming and len(mail_ids) !=0:
            break
        if len(mail_ids) == 0:
            comming = True
        if init_amount !=0 and init_amount !=len(mail_ids):
            break
        init_amount = len(mail_ids)
        
    if len(mail_ids) == 0:
        return "Error No Email Received"

    success = False
    for i in mail_ids:
        conn.store(i, '+FLAGS', '\Seen') 
        status, data = conn.fetch(i, '(RFC822)')
        # print(data)
        
        link = None
        try:
            if  str(data).count("color: #ffffff") > 3:
                email_ = str(data).split("-webkit-border-radius")[1].split("Verify Now ")[0]
                link = email_.split('"><a href=3D"')[1].split(' style=3D"color: #ffffff;')[0].replace("=\\r\\n","").replace("3D","")
                # return link
                print(link)
            else:
                # print(str(data))
                email_ = str(data).replace("=\\r\\n","").split("Verify Now ")[0].split("on your account.")[1].replace("\\n","")
                link = email_.replace("\\r","").strip()
                print(link)
        except:
            print("invalid format")
        conn.store(i, '+FLAGS', '\Seen')
        if link != None:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            # conn.store(data[i].replace(' ',','),'+FLAGS','\Seen')
            driver.get(link)
            while True:
                try:
                    title = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div[2]/div').get_attribute("innerHTML")
                    print(title)
                    break
                except:
                    time.sleep(1)
            try:
                is_verified = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/main/div/div[2]/div/div[3]/div/div').get_attribute("innerHTML")
                print(is_verified.split("<br>")[0])
                success = True
                continue
            except:
                pass
            try:
                is_verified = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/main/div/div[2]/div/div/div/div').get_attribute("innerHTML")
                print (is_verified.strip())
                continue
            except:
                pass
    driver.quit()
            
    if success:
        return "Success"
    return "Error Verification Failed"

def export_blocked_proxy(data):
    with open("blocked_proxy.txt","a") as f:
        f.write("\n")
        f.write(data)


def page_one(driver, index):
    try:
        while True:
            try:
                btn_start = driver.find_element_by_xpath( '/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[2]/main/div[1]/div/div[3]/div[5]/div/button' )
                break
            except:
                time.sleep(1)
        btn_start.click()
        upgrade_status("[:--->> Open first page")
        #start first page
        while True:
            try:
                input_email = driver.find_element_by_xpath( '/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[2]/div[2]/div/div/div/input' )
                break                                        
            except:
                time.sleep(1)
        
        while True:
            input_password = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[2]/div[5]/div[1]/div/div/input')
            input_re_password = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[2]/div[5]/div[3]/input')
            global Password
            Password = generate_password(8)
            upgrade_status(Password)
            input_email.send_keys(list_agent[index]['Email'])
            input_password.clear()
            input_re_password.clear()
            input_password.send_keys(Password)
            input_re_password.send_keys(Password)
            while True:
                try:
                    btn_next = driver.find_element_by_xpath( '/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[5]/div[1]/div/div[3]/button' )
                    break
                except:
                    time.sleep(1)
            btn_next.click()
            upgrade_status("[:--->> Input Email and password.")
            try:
                msg_error = driver.find_element_by_xpath( '//html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[1]/div[1]/div/div[2]/div' ).get_attribute('innerHTML')
                upgrade_status(msg_error)
                if len(msg_error) > 10:
                    return "Error " + msg_error
                break
            except:
                time.sleep(1)
        return "Success"

    except:
        return "Unknown Error_1"



def page_second(driver, index):
    time.sleep(3)
    try:
        sudden_error = driver.find_element_by_xpath('//*[@id="ember52"]/div[2]/div/div/div/div').get_attribute('innerHTML')
        return sudden_error
    except:
        pass
    upgrade_status("[:--->> Checking Captcha")
    time.sleep(4)


    return('manual captcha!!')


    try:
        while True:
            while True:
                try:
                    captcha_container = driver.find_element_by_xpath('//*[@id="ember-root"]/div[4]').get_attribute("style")
                    break
                except:
                    time.sleep(1)

            if not "visibility: visible;" in captcha_container:
                upgrade_status("[:--->> Captcha didn't re-actived")
                break
            upgrade_status("[:--->> Captcha activated.")
            token = pass_captcha(driver)
            time.sleep(1)
            driver.execute_script('widgetVerified("%s")'%token)
            driver.execute_script('document.querySelectorAll("#ember-root > div")[3].style.visibility="hidden"')
            upgrade_status("[:--->> Excellent! avoid captcha!")
            time.sleep(3)
        try:
            msg_error = driver.find_element_by_xpath('//*[@id="ember33"]/div[2]/div').get_attribute("innerHTML")
            upgrade_status("[:--->> Checking error")
            upgrade_status(msg_error)
            if len(msg_error) > 10:
                return "Error " + msg_error
        except:
            pass
        try:
            msg_error = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[1]/div[1]/div/div[2]/div').get_attribute("innerHTML")
            upgrade_status("[:--->> Checking error")
            upgrade_status(msg_error)
            if len(msg_error) > 10:
                return "Error " + msg_error
        except:
            pass
        time.sleep(5)

        return "Success"

    except:
        time.sleep(5)
        return "Error 'A error from sony'"
   
def page_third(driver, index):
    try:
        while True:
            try:
                select_state = Select(driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[3]/div/div[2]/div[1]/div[2]/div[3]/div/select'))
                break
            except:
                time.sleep(1)
        upgrade_status("[:--->> Input Birthday and State")
        time.sleep(2)
        select_country = Select(driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[3]/div/div[2]/div[1]/div[1]/div[2]/div/select'))                                   
        select_country.select_by_visible_text("United States")
        time.sleep(2)
        select_state = Select(driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[3]/div/div[2]/div[1]/div[2]/div[3]/div/select'))
        select_state.select_by_visible_text(list_agent[index]['State'])
        select_month = Select(driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[3]/div/div[2]/div[4]/fieldset/div/div[1]/div/select'))
                                                            
        select_day = Select(driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[3]/div/div[2]/div[4]/fieldset/div/div[3]/div/select'))
        select_year = Select(driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[3]/div/div[2]/div[4]/fieldset/div/div[5]/div/select'))
        birth_month = randint(1,12)
        birth_year = randint(1978,1990)
        birth_day = randint(1,28)
        select_month.select_by_value(str(birth_month))
        select_day.select_by_value(str(birth_day))
        select_year.select_by_value(str(birth_year))
        global Birthday
        Birthday = str(birth_month) + "/" + str(birth_day) + "/" + str(birth_year)
        upgrade_status("[:--->> Save birth day")
        while True:
            try:
                btn_next = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[3]/div/div[5]/div[1]/div/div[3]/button')
                break
            except:
                time.sleep(1)
        btn_next.click()
        time.sleep(5)

        return "Success"
    except:
        time.sleep(5)
        return "Unknown Error 2"

def page_four(driver, index):
    # try:
    time.sleep(3)
    while True:
        try:
            btn_agree = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[4]/div/div[5]/div[1]/div/div[3]/button')
            break
        except:
            time.sleep(1)
    btn_agree.click()
    upgrade_status("[:--->> Agree with term of policy")
    # end third page
    time.sleep(2)
    try:
        err_msg = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[4]/div/div[1]/div[1]/div/div[2]/div').get_attribute('innerHTML')
        upgrade_status(err_msg)
        if (len(err_msg) > 10):
            time.sleep(5)
            return "Error " + err_msg
    except:
        pass
    while True:
        try:
            btn_vrified = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/main/div/div[1]/div/div[2]/div[5]/div/button')
            break
        except:
            time.sleep(1)
    upgrade_status("[:--->> Email verify start..")
    verify_result = email_verify()
    if  verify_result == "Success":
        btn_vrified.click()
        time.sleep(5)
        return "Success"
    else:
        upgrade_status("[:--->> Verify Failed")
        time.sleep(5)
        return "Error " + verify_result



def page_five(driver, index):
    
    while True:
        try:
            skip_buttons = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/main/div/div[3]/div[5]/div[1]/button')
            skip_buttons.click()                            
            break
        except:
            time.sleep(1)
    time.sleep(5)
    return "Success"
    
def page_six(driver, index):
        while True:
            try:
                skip_buttons = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[1]/div/div[2]/div[3]/div[1]/button')
                skip_buttons.click()                        
                break
            except:
                time.sleep(1)
        time.sleep(5)
        return "Success"

    

def page_seven(driver, index):
    try:
        driver.get("https://id.sonyentertainmentnetwork.com/id/management/")
        time.sleep(6)
        while True:
            try:
                btn_edit_PSN = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/ul/li[2]/ul/li[1]/div/button')
                print("find button")                         
                time.sleep(5)
                driver.execute_script("arguments[0].click();", btn_edit_PSN)
                break
            except:
                print("finding button")
                time.sleep(1)
        time.sleep(5)
        try:
            input_password = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div[3]/div/div/div/div/div/div[2]/div/div/main/div/div[2]/div/form/div[1]/div[2]/div/div/div/input')
            input_password.send_keys(Password)
            btn_finish = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div[3]/div/div/div/div/div/div[2]/div/div/main/div/div[2]/div/form/div[3]/div/button')
            btn_finish.click()                          
        except:
            upgrade_status("No request password")

        while True:
            try:
                btn_next = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div[2]/div/div[3]/div/div/div/div/main/div/div/div[2]/div[2]/div[3]/div/div/button')
                break                                    
            except:
                time.sleep(1)
        btn_next.click()

        while True:
            try:
                btn_start = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/main/div/div[3]/div[11]/div/button')
                break
            except:
                time.sleep(1)
        btn_start.click()
        while True:
            try:
                input_city= driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[1]/div/div[2]/div/fieldset/div[2]/div/div/div/input')
                break
            except:
                time.sleep(1)
        input_city.send_keys(list_agent[index]["City"])
        input_postalcode = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[1]/div/div[2]/div/fieldset/div[8]/div/div/div/input')
        input_postalcode.send_keys(list_agent[index]["Postal Code"])
        btn_next = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[1]/div/div[5]/div[1]/div/div[3]/button')
        btn_next.click()

        while True:
            try:
                default_id = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[4]/div[1]/button')
                break
            except:
                time.sleep(1)
        uniqure_id = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[4]/div[1]/button/span').get_attribute('innerHTML')
        global Online_id
        Online_id = uniqure_id
        default_id.click()
        input_firstname = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[2]/div[3]/div[2]/div/div/div/input')
        input_lastname = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[2]/div[3]/div[3]/div/div/div/input')
        input_firstname.send_keys(list_agent[index]['First Name'])
        input_lastname.send_keys(list_agent[index]['Last Name'])
        btn_save = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div[1]/div[3]/main/div[2]/div/div[5]/div[1]/div/div[3]/button')
        btn_save.click()
        time.sleep(5)
        try:
            input_password = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div[3]/div/div/div/div/div/div[2]/div/div/main/div/div[2]/div/form/div[1]/div[2]/div/div/div/input')
            input_password.send_keys(Password)
            btn_finish = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div/div/div[3]/div/div/div/div/div/div[2]/div/div/main/div/div[2]/div/form/div[3]/div/button')
            btn_finish.click()
        except:
            upgrade_status("No request password")

        time.sleep(5)
        
        return "Success"

    except:
        time.sleep(5)
        return "Unknown Error 6"


def _loop(index):

    url = "https://id.sonyentertainmentnetwork.com/create_account/"
    
    proxy_index = randint(0,len(list_proxy) -1)
    
    while True:
        driver = Create_driver(list_proxy[randint(0,proxy_index)]['IP'] + ":"  + list_proxy[randint(0,proxy_index)]['Port'])
        driver.get(url)
        time.sleep(5)
        upgrade_status("start")
        try:
            msg_no_internet = driver.find_element_by_xpath('//*[@id="main-message"]/p').get_attribute('innerHTML')
            driver.close()
            upgrade_status(msg_no_internet)
            upgrade_status("1")
            upgrade_status("damaged proxy" + list_proxy[proxy_index]['IP'])
            damaged_proxy_list.append( list_proxy[proxy_index]['IP'])
            while True:
                proxy_index = randint(0,len(list_proxy) -1)
                upgrade_status("2")
                doublicated = False
                for i in range(len(damaged_proxy_list)):
                    if proxy_index == damaged_proxy_list[i]:
                        doublicated = True
                        upgrade_status("3")
                        break
                if doublicated == False:
                    upgrade_status("4")
                    break
        except:
            break

    
    time.sleep(2)
    result = page_one(driver,index)
    upgrade_status(result)
    if "Error" in result:
        save_all_data(Email = list_agent[index]["Email"],State = list_agent[index]["State"], Postal_code = list_agent[index]["Postal Code"], City = list_agent[index]["City"]  ,password = Password, status = result)
        driver.close()
        return
    result = page_second(driver, index)
    upgrade_status(result)
    if "Error" in result:
        save_all_data(Email = list_agent[index]["Email"],State = list_agent[index]["State"], Postal_code = list_agent[index]["Postal Code"], City = list_agent[index]["City"]  ,password = Password, status = result)
        driver.close()
        return
    result = page_third(driver, index)
    upgrade_status(result)
    if "Error" in result:
        save_all_data(Email = list_agent[index]["Email"],State = list_agent[index]["State"], Postal_code = list_agent[index]["Postal Code"], City = list_agent[index]["City"]  ,password = Password, status = result)
        driver.close()
        return
    result =  page_four(driver, index)
    upgrade_status(result)
    if "Error" in result:
        save_all_data(Email = list_agent[index]["Email"],State = list_agent[index]["State"], Postal_code = list_agent[index]["Postal Code"], City = list_agent[index]["City"]  ,password = Password, status = result)
        driver.close()
        return
    result =  page_five(driver, index)
    upgrade_status(result)
    if "Error" in result:
        save_all_data(Email = list_agent[index]["Email"],State = list_agent[index]["State"], Postal_code = list_agent[index]["Postal Code"], City = list_agent[index]["City"]  ,password = Password, status = result)
        driver.close()
        return
    result =  page_six(driver, index)
    upgrade_status(result)
    if "Error" in result:
        save_all_data(Email = list_agent[index]["Email"],State = list_agent[index]["State"], Postal_code = list_agent[index]["Postal Code"], City = list_agent[index]["City"]  ,password = Password, status = result)
        driver.close()
        return
    result = page_seven(driver,index)
    if "Error" in result:
        save_all_data(Email = list_agent[index]["Email"],State = list_agent[index]["State"], Postal_code = list_agent[index]["Postal Code"], City = list_agent[index]["City"]  ,password = Password, status = result)
        driver.close()
        return
    upgrade_status("[:--->> Saving result data...")
    save_all_data(Email = list_agent[index]["Email"],
        firstname = list_agent[index]["First Name"],
        lastname = list_agent[index]["Last Name"],
        password = Password,
        birth_day = Birthday,
        online_id = Online_id,
        email_pwd = list_agent[index]["Email Pwd"],
        proxy = list_agent[index]['Proxy Ip'] + ":" +list_agent[index]['Proxy Port'],
        status = "Success",
        City = list_agent[index]["City"],
        State = list_agent[index]["State"],
        Postal_code = list_agent[index]["Postal Code"])
    driver.close()
    return


def upgrade_status(status):
    print(status)
    T.insert(END, status +  "\n")
    T.see("end")
    root.update_idletasks()


def disable_status():

    Entry_number_account['state'] = 'disable'
    Btn_start['state'] = 'disable'


def enable_status():
    Entry_number_account['state'] = 'normal'
    Btn_start['state'] = 'normal'



def Start():
    threading.Thread(target=main_loop).start()
def main_loop():
    # driver = Create_driver()
    # driver.get("https://id.sonyentertainmentnetwork.com/create_account/")
    # verify_result = email_verify(driver,list_agent[0]['Email'], list_agent[0]['Email Pwd'])
    # upgrade_status( verify_result )
    # _loop(1)
    # i = 1
    # for i in range (len()):
        # _loop(i)
    disable_status()
    if Entry_number_account.get() == "":
        messagebox.showerror("Error", "Please input number of accounts")
        return
    total_number = int(Entry_number_account.get())
    
    try:
        if total_number < 0:
            messagebox.showerror("Error", "Number of account should above 1")
    except:
        messagebox.showerror("Error", "Invalid input")
    Create_agent_list(total_number)
    print(list_agent)
    for i in range(total_number):
        _loop(i)

    file_directory = os.path.dirname(os.path.abspath(__file__))
    export_logfile(T.get('1.0', END))
    for i in range(len(damaged_proxy_list)):
        export_blocked_proxy(str(damaged_proxy_list[i]))
    upgrade_status("********All task Finished******** \n result data saved in %s\ acount.csv"%file_directory)   
    enable_status()




if __name__ == '__main__':

    list_city = []
    list_agent = []
    list_proxy = []
    damaged_proxy_list = []
    Password =''
    read_config_data()
    read_proxy_data()
    print(len(list_proxy))
    city_limit = len(list_city)-1
    print(city_limit)
    root = Tk() 
    root.geometry("700x250")
    root.title("Sony account Creator")
    root.wm_attributes("-topmost", 1)


    root.grid_columnconfigure(0, weight = 1)
    root.grid_columnconfigure(1, weight = 3)
    root.grid_columnconfigure(2, weight = 1)

    Label_number_account =  Label(root, text="Number of Accounts", width = 20)
    Label_number_account.grid(row = 1, column = 0 , sticky = E)
    Entry_number_account =  Entry(root, bd =2, width = 30)
    Entry_number_account.grid(row = 1, column = 1)


    Btn_start = Button(root, width = 20, text = "Start", command = lambda: Start() )
    Btn_start.grid( row = 1, column = 2, sticky = W + E)
    Btn_start.grid(padx=30, pady=5)

    Label_status =  Label(root, text="Current status", width = 20)
    Label_status.grid(row = 2, column = 0 , sticky = E)

    output_status = Frame(root,width = 700,height = 10, background = "pink")
    output_status.grid(columnspan = 5, row = 3,rowspan = 8, sticky = W+E,padx=20, pady=5)

    S = Scrollbar(output_status)
    T = Text(output_status, height=10, width=700, state="normal")
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=TOP, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)


    mainloop()


