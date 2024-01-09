from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

all_links = []

driver = webdriver.Firefox()
driver.get("https://gamebanana.com/mods/cats/6800")
driver.implicitly_wait(1)

cookies = driver.find_element(by=By.CLASS_NAME, value="fc-cta-consent")
cookies.click()

cog_icon = driver.find_element(by=By.CLASS_NAME,value="MiscIcon.CogIcon")
cog_icon.click()

page_input = driver.find_element(by=By.CLASS_NAME,value="control")

for i in range(1,126):
    page_input.send_keys(str(i)+"\uE007")
    time.sleep(7)
    links = driver.find_elements(by=By.CLASS_NAME, value="Name")
    for link in links:
        all_links.append(link.get_attribute("href"))
    
p = 0
with open("C:/Users/ethan/Desktop/celestemods.txt","w") as cmods:
    for link in all_links:
        cmods.write("%s\n" % link)
        p+=1
    cmods.write("%s maps" % p)