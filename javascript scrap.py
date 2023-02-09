import time 
import requests
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import datetime

class SprawdzajStrone():
    def __init__(self):
        self.poprzedni_tekst = ''

    def sprawdz_strone(self):
        # start by defining the options 
        options = webdriver.ChromeOptions() 
        options.headless = True # it's more scalable to work in headless mode 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # this returns the path web driver downloaded 
        chrome_service = Service(executable_path='C:\Program Files\Chrome Driver\chromedriver.exe') 
        # pass the defined options and service objects to initialize the web driver 
        driver = Chrome(ChromeDriverManager().install(),options=options) 
        driver.implicitly_wait(5)
        url = "https://www.dentalday.pl/szkolenia/pedodoncja-modul-i-leczenie-endodontyczne-u-dzieci-3-edycja.html" 
        driver.get(url) 
        time.sleep(5)
        content = driver.find_elements(By.CLASS_NAME, "single-tile-inner")
        for tekst in content:      
            if tekst.text.find("Wolne miejsca") != -1:
                print(datetime.datetime.now().strftime('%H:%M:%S') + ": " + tekst.text) 
                if tekst.text != self.poprzedni_tekst:
                    self.wiadomosc = "Zmiana!\nByło: " + str(self.poprzedni_tekst) + "\nJest: " + tekst.text
                    self.wyslij_powiadomienie(self.wiadomosc)
                    self.poprzedni_tekst = tekst.text
        driver.close()
    
    def wyslij_powiadomienie(self, tekst):
        self.url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={tekst}"
        print(requests.get(self.url).json())
    
if __name__ == '__main__':
    TOKEN = "5816344668:AAGgs9IK0iAiWG603pwetbOSdCPxL6zsia8"
    CHAT_ID = "5526684558"
    sprawdzajStrone = SprawdzajStrone()

    while True:
        sprawdzajStrone.sprawdz_strone()
        time.sleep(50)