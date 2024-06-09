from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

SIMILAR_ACCOUNT = "thenotoriousmma" 
USERNAME = "username"
PASSWORD = "password"


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)
        time.sleep(4.2)

        
        try:
            cookie_warning = self.driver.find_element(By.XPATH, "//button[text()='Accept']")
            cookie_warning.click()
        except NoSuchElementException:
            print("Cookie warning not found or already dismissed.")

       
        try:
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")
            username_input.send_keys(USERNAME)
            password_input.send_keys(PASSWORD)
            password_input.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print("Username or password input fields not found.")

        time.sleep(4.3)

      
        try:
            save_login_prompt = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            save_login_prompt.click()
        except NoSuchElementException:
            print("Save login prompt not found or already handled.")

        time.sleep(3.7)

        
        try:
            notifications_prompt = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            notifications_prompt.click()
        except NoSuchElementException:
            print("Notifications prompt not found or already handled.")

    def find_followers(self):
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")

        try:
           
            modal = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'] ul"))
            )

           
            for i in range(5):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)

        except NoSuchElementException:
            print("Followers modal not found.")
        except TimeoutException:
            print("Followers modal did not load in time.")

    def follow(self):
        try:
          
            follow_buttons = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[text()='Follow']"))
            )

           
            for i, button in enumerate(follow_buttons[:5]):
                try:
                    
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(3)
                    button.click()
                    print(f"Followed {i+4} user.")
                    time.sleep(5) 
                except ElementClickInterceptedException:
                    print("ElementClickInterceptedException: Trying alternative method...")
                   
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(3)
                except Exception as e:
                    print(f"Error clicking follow button: {str(e)}")

        except NoSuchElementException:
            print("Follow buttons not found.")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    bot = InstaFollower()
    try:
        bot.login()
        bot.find_followers()
        bot.follow()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        bot.close()
