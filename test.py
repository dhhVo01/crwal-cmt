import sys
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument("--disable-notifications")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

url = sys.argv[1]

#driver.implicitly_wait(10)
driver.get(url)

username = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.ID, "email"))
password = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.ID, "pass"))
username.send_keys(os.getenv("EMAIL"))
password.send_keys(os.getenv("PASSWORD"))
password.send_keys(Keys.ENTER)

xpath_feed = '//div[@role="feed"]'
xpath_show_classification = "//div/div/span[contains(text(), 'Phù hợp nhất')]"
xpath_show_all = "//div/div/div/span[contains(text(), 'Tất cả bình luận')]"
xpath_see_more = "//div/span/span[starts-with(text(), 'Xem thêm')]"
xpath_first_cmt = "//div[starts-with(@aria-label, 'Bình luận dưới tên')]"
xpath_first_replies_cmt = "//div[starts-with(@aria-label, 'Phản hồi bình luận của')]"

def remove_element(element):
    driver.execute_script(
                    """var element = arguments[0]; 
                    element.parentNode.removeChild(element);""", element)

time_start = time.time()
feed = WebDriverWait(driver, timeout=60).until(lambda d: d.find_element(By.XPATH, xpath_feed))
time.sleep(10)
feed = driver.find_element(By.XPATH, xpath_feed)
if (feed.is_displayed()):
     remove_element(feed)

def show_all_cmt(xpath_show_classification, xpath_show_all):
    try:
        show_classification = driver.find_element(By.XPATH, xpath_show_classification)
        show_classification.click()
        time.sleep(2)
        show_all = driver.find_element(By.XPATH, xpath_show_all)
        show_all.click()
        time.sleep(3)
    except:
        show_all_cmt(xpath_show_classification, xpath_show_all)
    else: return
def find_button_see_more(class_name):
    xpath = '//div[@class="' + class_name +'"]'
    tmp = [div for div in driver.find_elements(By.XPATH, xpath)]
    if tmp == []: return False
    return tmp[0]
def see_more_cmt(class_name):
    cnt = 1
    button_see_more = find_button_see_more(class_name)
    while (button_see_more != False):
          try:
              button_see_more.click()
          except:
              cnt+=1
              time.sleep(2)
              if cnt == 5:
                  time.sleep(5)
              button_see_more = find_button_see_more(class_name)
def get_list_element_cmt(xpath_first_cmt):
    first_cmt = driver.find_element(By.XPATH, xpath_first_cmt)
    class_cmt = first_cmt.get_attribute("class")
    #see_more_content_cmt(class_cmt)
    xpath_cmt = "//div[@class='" + class_cmt + "']"
    return driver.find_elements(By.XPATH, xpath_cmt)

def get_class_see_more_cmt(xpath_see_more):
    e_child = driver.find_element(By.XPATH, xpath_see_more)
    e = e_child.find_element(By.XPATH, "./../..")
    return e.get_attribute("class")
def get_class_cmt(xpath):
    e = driver.find_element(By.XPATH, xpath)
    return e.get_attribute("class")
def get_class_replies_cmt(xpath):
    e = driver.find_elements(By.XPATH, xpath)
    if e != []:
        return e[0].get_attribute("class")
    else: return ""
def get_data_cmt(e):
    div_link_profile = e.find_element(By.CSS_SELECTOR, 'div:first-child')
    class_div_link_profile = div_link_profile.get_attribute("class")
    link_profile = div_link_profile.find_element(By.TAG_NAME, "a").get_attribute("href")
    div_content_cmt = e.find_element(By.CSS_SELECTOR, 'div[class="'+class_div_link_profile+'"]+div')
    class_div_content_cmt = div_content_cmt.get_attribute("class")
    list_div_child_content_cmt = div_content_cmt.find_elements(By.CSS_SELECTOR, 'div[class="'+class_div_content_cmt+'"]>div')
    div_child_1 = div_content_cmt.find_element(By.CSS_SELECTOR, "div:first-child")
    div_child_2 = div_child_1.find_element(By.CSS_SELECTOR, "div:first-child")
    badges = div_child_2.find_elements(By.XPATH, "//div[starts-with(@aria-label, 'Identity Badges')]")
    if badges != []:
        remove_element(badges[0])
    div_child_3 = div_child_2.find_element(By.CSS_SELECTOR, "div:first-child")
    div_child_4 = div_child_3.find_element(By.CSS_SELECTOR, "div:first-child")
    div_result = div_child_4
    if len(list_div_child_content_cmt) == 1:
        div_child_5 = div_child_4.find_element(By.CSS_SELECTOR, "div:first-child")
        div_child_6 = div_child_5.find_element(By.CSS_SELECTOR, "div:first-child")
        div_result = div_child_6
    name = div_result.find_element(By.CSS_SELECTOR, "span:first-child").text
    class_div_result = div_result.get_attribute("class")
    text_cmt = div_result.find_element(By.CSS_SELECTOR, 'div[class="'+class_div_result+'"]>div').text
    return link_profile, name, text_cmt
def get_metadata_cmt(xpath_cmt, class_name_replies_cmt):
    col_link_profile = []
    col_name = []
    col_cmt_text = []
    #xpath_cmt = '//div[@class="' + class_name_cmt +'"]'
    xpath_replies_cmt = '//div[@class="' + class_name_replies_cmt +'"]'
    list_cmt = driver.find_elements(By.XPATH, xpath_cmt)
    list_cmt_replies = driver.find_elements(By.XPATH, xpath_replies_cmt)
    print("list_cmt:", len(list_cmt),"list_replies_cmt: ",len(list_cmt_replies))
    list_e = list_cmt + list_cmt_replies
    print("list_e:", len(list_e))
    for e in list_e:
        link_profile, name, text_cmt = get_data_cmt(e)
        col_link_profile.append(link_profile)
        col_name.append(name)
        col_cmt_text.append(text_cmt)
    return col_link_profile, col_name, col_cmt_text

show_all_cmt(xpath_show_classification, xpath_show_all)
see_more_cmt(get_class_see_more_cmt(xpath_see_more))
arr = []
col_link_profile = []
col_name = []
col_cmt_text = []
col_link_profile, col_name, col_cmt_text = get_metadata_cmt(xpath_first_cmt, get_class_replies_cmt(xpath_first_replies_cmt))
arr.append(col_link_profile)
arr.append(col_name)
arr.append(col_cmt_text)
columns = ["link_profile", "name", "text_comment"]
pd.DataFrame(arr, index = columns).T.to_excel("C:/Users/vohuy/Desktop/crawl_cmt.xlsx")


time.sleep(2)
driver.quit()

result = '{"status": true, "url":"' + url + '"}'

print(result)