from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Scopus_Connection():
    def __init__(self):
        self.path = " "
    def log_in(self,user_name,password):
        self.driver = webdriver.Chrome(self.path)
        self.driver.get("https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Ainst_assoc&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3D5626333045bc43c991f10185566756c4&state=checkAccessLogin%7CtxId%3DC1B4D4ED9292EC0A5E508150DB3784F4.i-0cdb3fa8ee9b5f411%3A4&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS")
        self.email = user_name
        self.password = password
        first_page_login = self.driver.find_element(By.NAME,"els_institution")
        first_page_login.send_keys(self.email)
        try:
            continue1 = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.NAME, 'action')))
            continue1.click()
            continue2 = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.ID, 'bdd-elsPrimaryBtn')))
            continue2.click()
            user_name = self.driver.find_element(By.ID, "username")
            password = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            user_name.send_keys(self.email )
            password.send_keys(self.password)
            time.sleep(5)
            password.send_keys(Keys.RETURN)
        except:
            pass
        return self.driver

    def search_article(self,keyword):
        try:
            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, 'flex-grow-1')))
            search = self.driver.find_element(By.CLASS_NAME, 'flex-grow-1')
            search.send_keys(keyword)
            time.sleep(3)
            search.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.LINK_TEXT,"Show all abstracts")))
            self.driver.find_element(By.LINK_TEXT,"Show all abstracts").click()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "srchResultsList")))
            result_list = self.driver.find_elements(By.CLASS_NAME,"searchArea")
            abstract_list = self.driver.find_elements(By.XPATH,"//*[@class='panel-collapse collapse displayNone']/td")
            print(len(abstract_list))

            for result in result_list:
                try:
                    title = result.find_element(By.CLASS_NAME,"ddmDocTitle").text
                    date = result.find_element(By.CLASS_NAME,"ddmPubYr").text
                    print(title)
                except:
                    continue
            for abstract in abstract_list:
                try:
                    print(abstract.find_element(By.CLASS_NAME,"txt").text)
                except:
                    continue
            time.sleep(30)
        except Exception as e:
            print(e)
    def stop_section(self):
        self.driver.close()
conn = Scopus_Connection()
conn.log_in(" "," ")
conn.search_article(" ")
conn.stop_section()
