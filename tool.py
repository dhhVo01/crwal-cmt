import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
url = sys.argv[1]
driver.get(url)
time.sleep(5)
driver.quit()
print(url)