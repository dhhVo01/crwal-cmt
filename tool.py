import sys
from selenium import webdriver
import chromedriver_autoinstaller
import time
from selenium.webdriver.common.by import By
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
url = sys.argv[1]
driver.get(url)
time.sleep(5)
driver.quit()
print(url)