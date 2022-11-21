import sys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
service = Service(executable_path="/usr/bin/google-chrome")
driver = webdriver.Chrome(service=service)
url = sys.argv[1]
driver.get(url)
time.sleep(5)
driver.quit()
print(url)