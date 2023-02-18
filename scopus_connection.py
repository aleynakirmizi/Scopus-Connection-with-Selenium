from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_connection import Db_Connection
import time

class Scopus_Connection():
    def __init__(self):
        self.path = ""
        self.keyword=''
        self.db= Db_Connection()
        self.db.build_connection('database.db')
        self.db.create_table()
        self.class_name = ''
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
            user_name.send_keys(self.email)
            user_name.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.NAME, 'j_username')))
            user_confirm = self.driver.find_element(By.NAME, 'j_username')
            user_pass = self.driver.find_element(By.NAME, 'j_password')
            user_confirm.clear()
            user_confirm.send_keys("")
            user_pass.send_keys(self.password)
            time.sleep(5)
            user_pass.send_keys(Keys.RETURN)

        except Exception as e:
            print("log in error ")
            print(e)
        return self.driver
    def get_informations(self,keyword):
        # title_np_list = np.array()
        try:
            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.LINK_TEXT, "Show all abstracts")))
            self.driver.find_element(By.LINK_TEXT, "Show all abstracts").click()
            time.sleep(10)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "srchResultsList")))
            result_list = self.driver.find_elements(By.CLASS_NAME, "searchArea")
            abstract_list = self.driver.find_elements(By.XPATH, "//*[@class='panel-collapse collapse displayNone']/td")
            for result,abstract in zip(result_list,abstract_list):
                try:
                    title = result.find_element(By.CLASS_NAME, "ddmDocTitle").text
                except:
                    title = 0
                    continue
                try:
                    date = result.find_element(By.CLASS_NAME, "ddmPubYr").text
                except:
                    date = 0
                    continue
                try:
                    abstract = abstract.find_element(By.CLASS_NAME, "txt").text
                except:
                    abstract = 0
                    continue
                self.db.add_article(title,keyword,abstract,date,self.class_name)
            time.sleep(25)
        except Exception as e:
               print("get information error ")
               print(e)
        return result_list,abstract_list

    def search_article(self,keyword):
        self.keyword = keyword
        try:
            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, 'flex-grow-1')))
            search = self.driver.find_element(By.CLASS_NAME, 'flex-grow-1')
            search.send_keys(keyword)
            time.sleep(3)
            search.send_keys(Keys.RETURN)
            self.get_informations(keyword)
        except Exception as e:
            print("search article error ")
            print(e)
        self.driver.back()
        WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, 'flex-grow-1')))
        search = self.driver.find_element(By.CLASS_NAME, 'flex-grow-1')
        search.clear()
    def advanced_search(self,keyword,year):
        try:
            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="documents-tab-panel"]/div/form/div[2]/div[1]/a')))
            self.driver.find_element(By.XPATH, '//*[@id="documents-tab-panel"]/div/form/div[2]/div[1]/a').click()
            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#SCAdvSearchInputBox')))
            adv_search_entry = self.driver.find_element(By.CSS_SELECTOR, '#SCAdvSearchInputBox').click()
            WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#searchfield')))
            adv_search=self.driver.find_element(By.CSS_SELECTOR, '#searchfield')
            adv_search.clear()
            query = f"TITLE-ABS ( {keyword} ) AND ( LIMIT-TO ( PUBYEAR , {year} )"
            adv_search.send_keys(query)
            adv_search.send_keys(Keys.RETURN)
            self.get_informations(keyword)
            time.sleep(5)
        except Exception as e:
            print("advance search error ")
        self.driver.back()
        WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="documents-tab-panel"]/div/form/div[2]/div[1]/a')))
        adv_search.find_element(By.XPATH, '//*[@id="documents-tab-panel"]/div/form/div[2]/div[1]/a')
        adv_search.clear()

    def stop_section(self):
        self.driver.close()

conn = Scopus_Connection()
conn.log_in()
# list_search=["digital twin","virtual"]
# for keywords in list_search:
#     conn.search_article(keywords)
conn.advanced_search("digital twin",2023)
conn.stop_section()
