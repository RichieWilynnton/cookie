from http import cookies
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import keyboard as kb

import time
from dotenv import load_dotenv
import os 

load_dotenv()

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service = service)

with open("save.txt", "r", encoding='utf-8') as fr:
    saveCode = fr.read()

driver.get("https://orteil.dashnet.org/cookieclicker/")
actions = ActionChains(driver)
def selectLanguage():
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "languageSelectHeader"))
    )
    selectEnglishButton = driver.find_element(By.ID, "langSelect-EN")
    selectEnglishButton.click()

def loadSave():
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "prefsButton"))
    )
    actions.key_down(Keys.CONTROL).send_keys('o').key_up(Keys.CONTROL).perform()

    textAreaPrompt = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "textareaPrompt"))
    )
    textAreaPrompt.send_keys(saveCode + Keys.ENTER)



def clickCookie():
    cookie_id = "bigCookie"
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, cookie_id))
    )
    cookie = driver.find_element(By.ID, cookie_id)
    
    while True:
        if kb.is_pressed('q'):
            break

        cookie.click()
        cookiesCount = driver.find_element(By.ID, "cookies").text.split(" ")[0]
        cookiesCount = int(cookiesCount.replace(",", ""))

        unlockedProducts = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
        unlockedCrateProducts = driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")

        unlockedProducts += unlockedCrateProducts
        print(len(unlockedProducts))

        for product in unlockedProducts:
            # productPrice = product.find_element(By.CLASS_NAME, "price").text.replace(",", "")
            # if not productPrice.isdigit():
            #     continue
            # productPrice = int(productPrice)
            try:
                # if cookiesCount >= productPrice:
                product.click()
            except:
                continue
        
def save():
    options = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, "subButton"))
    )
    options.click()
    exportSave = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Export save')]"))
    )
    exportSave.click()
    textarea = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "textareaPrompt"))
    )
    with open("save.txt", "w", encoding='utf-8') as fw:
        fw.write(textarea.text)
    print("Saved")



selectLanguage()
loadSave()

clickCookie()
save()
time.sleep(3)




driver.quit()