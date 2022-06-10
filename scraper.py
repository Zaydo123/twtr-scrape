from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)
driver.minimize_window()
with open('tokens.txt','r+') as f:
    tokens = f.read().split('\n')
    print(tokens)


limit = int(input('how many usernames would you like to scrape: '))
target=input('target: ')

def start():
    global token
    token = random.choice(tokens)
    driver.get('https://twitter.com/@elonmusk')
    driver.add_cookie({"name": "auth_token", "value": token, 'sameSite': 'Strict'})
    driver.refresh()

start() 

def testTokens():
    global token
    try:
        def getText():
            text = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div/div[1]').text
            return text
        text = getText()
        while text.find('Please verify your account')!=-1 or text.find('Enter')!=-1:
            text = getText()
            print('locked: '+token)
            tokens.remove(token)
            if len(tokens)==0:
                print('no active tokens left')
                quit()
            token = random.choice(tokens)
            driver.add_cookie({"name": "auth_token", "value": token, 'sameSite': 'Strict'})
            driver.get('https://twitter.com')
            time.sleep(2)
    except Exception as e:
        if(str(e).find('no such element')!=-1):
            print('no such element')
        else:
            print(e)
            print('retrying')
            time.sleep(5)
            testTokens()
time.sleep(2)
testTokens()

driver.get('https://twitter.com/'+target+'/followers')
time.sleep(4)
usernames = []
i=0
time_increment = 1
def parse():
    global time_increment
    global i
    try:
        print('usernames length : ',len(usernames))
        while len(usernames)<limit:
            i+=1
            if(i>18):
                i=1
            child = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div['+str(i)+']/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span')
            if child.text not in usernames: 
                usernames.append(child.text)
            else:
                print('usernames length : ',len(usernames))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(time_increment)
        print('usernames length : ',len(usernames))
    except Exception as e:
        if str(e).find('no such element')!=-1:
            time_increment+=.1
            print(time_increment)
            parse()
        else:
            print(e)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            parse()
parse()
driver.quit()
with open('output.txt','a+') as f:
    for i in usernames:
        #get last element from usernames list
        if(i==usernames[len(usernames)-1]):
            f.write(i)
        else:
            f.write(i+'\n')

