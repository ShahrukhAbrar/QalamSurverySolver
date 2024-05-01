import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

def feedback_sentence():
    with open('feedback.txt', 'r') as file:
        feedback = file.readlines()
    feedback = [sentence.strip() for sentence in feedback]
    random_sentence = random.choice(feedback)
    return random_sentence


USERNAME = 'sabrar.bese22mcs'
PASSWORD = 'student@4567'

driver = webdriver.Chrome()
driver.get('https://qalam.nust.edu.pk')

usernameField = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "login")))
usernameField.send_keys(USERNAME)
passwField = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "password")))
passwField.send_keys(PASSWORD)
passwField.send_keys(Keys.RETURN)

sleep(5)

surveryElement = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.md-card")))
surveryElementLinks = surveryElement.find_elements(By.XPATH,".//descendant::a[@href]")

with open('survey_links.txt', 'w') as file:
    for i in surveryElementLinks:
        link = i.get_attribute('href')
        if link == 'https://qalam.nust.edu.pk/student/qa/feedback#':
            continue
        file.write(link + '\n')


with open('survey_links.txt', 'r') as file:
    for link in file:
        driver.get(link)
        sleep(5)        #added delay here to make sure pages loades properly (helps with slow internet speeds)

        try:
            xpath_survey_completed = "//div[@class='md-card']//div[contains(text(), 'Survey is submitted.')]"
            completed_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_survey_completed)))
            print("Survey is already submitted.")
            continue

        finally:
            partial_heading_text = "Teacher Evaluation Form"
            xpath_expression = f"//div[@class='md-card-content']//h3[contains(text(), '{partial_heading_text}')]/ancestor::div[@class='md-card-content']"
            target_div = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
            action = ActionChains(driver)
            action.move_to_element(target_div).click().perform()


            for _ in range(8):
                action.send_keys(Keys.TAB)
                action.perform()
                random_arrow_presses = random.randint(1, 3)
                for _ in range(random_arrow_presses):
                    action.send_keys(Keys.ARROW_RIGHT)
                    action.perform()

            action.send_keys(Keys.TAB)
            action.perform()     

            action.send_keys(feedback_sentence())
            action.perform()

            action.send_keys(Keys.TAB)
            action.perform()
            action.send_keys(Keys.RETURN)
            action.perform()

            sleep(5)   #added 5sec delay to make sure the form is properly submitted
            continue



print("\nAll Forms have been submitted.......\n")
print("Quitting")
driver.quit()