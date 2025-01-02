from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, time, json, string
import chromedriver
import requests
from bs4 import BeautifulSoup
from faker import Faker

def get_inbox(email):
    try:
        inbox = requests.get(f"http://haileyy.lol/get_inbox?email={email}").json()
        return inbox
    except:
        return []
    
def click_element(wdriver, by: By, value):
    try:
        button = WebDriverWait(wdriver, 5).until(
            EC.element_to_be_clickable((by, value))
        ).click()
    except:
        pass

def keys_element(wdriver, by: By, value, text):
    try:
        button = WebDriverWait(wdriver, 5).until(
            EC.element_to_be_clickable((by, value))
        ).send_keys(text)
    except:
        pass
    
def create_aliexpress_account(region="United Kingdom", address=None, product=None, email=None, password=None, color=None, proxy=None, card=None):
    if email is None:
        email = ""
        for i in range(6):
            email += random.choice(string.ascii_lowercase+string.digits)
        email += "@"
        for i in range(6):
            email += random.choice(string.ascii_lowercase+string.digits)
        email += ".haileyy.lol"
        
    if password is None:
        password = ""
        for i in range(8):
            password += random.choice(string.ascii_lowercase+string.digits)
    
    driver = None
    
    if proxy is not None:
        driver = chromedriver.start_chrome_driver(proxy=proxy['ip'], proxyport=proxy['port'], username=proxy['username'], password=proxy['password'])
    else:
        driver = chromedriver.start_chrome_driver()
        
    driver.get("https://login.aliexpress.com/")
    time.sleep(1.5)
    keys_element(driver, By.CLASS_NAME, "cosmos-input", email)
    time.sleep(1)
    click_element(driver, By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/span[2]/span")
    time.sleep(1)
    keys_element(driver, By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/div/span/input", region)
    time.sleep(1)
    click_element(driver, By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/div/ul/li/span/span")
    time.sleep(1)
    click_element(driver, By.XPATH, "/html/body/div[5]/div[2]/div/div[2]/div[3]/button[2]/span")
    time.sleep(3)
    click_element(driver, By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/div[3]/div[3]/button")
    time.sleep(2)
    keys_element(driver, By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/span/span[1]/input", password)
    time.sleep(0.5)
    click_element(driver, By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[4]/button")
    
    print("Please Complete The Captcha.")
    
    # TODO: Automate Swipe Captcha
    
    #iframe = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/div/iframe")
    #driver.switch_to.frame(iframe)
    
    #slider = driver.find_element(By.XPATH, "/html/body/center/div[1]/div/div/div/span")

    #action = ActionChains(driver)
    #action.click_and_hold(slider)

    #for offset in range(0, 400, 50):
    #    action.move_by_offset(random.randint(30, 70), random.randint(-2, 4))
    #    time.sleep(random.randint(1, 15)/100)

    #action.release().perform()
    
    #driver.switch_to.default_content()
    
    while len(get_inbox(email)) == 0:
        time.sleep(1)
    time.sleep(5)
    inbox = get_inbox(email)
    soup = BeautifulSoup(inbox[0]['Body'], 'html.parser')
    div = soup.find('div', class_='code')
    code = div.text.strip()
    print(code)
    for idx, char in enumerate(code):
        keys_element(driver, By.XPATH, f"/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/input[{idx+1}]", char)
        time.sleep(0.2)
    
    while driver.current_url != "https://www.aliexpress.com/":
        time.sleep(1)
        
    print(email, password)
    
    if card is not None:
        driver.get("https://www.aliexpress.com/p/wallet-ui/index.html")
        time.sleep(1.5)
        click_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[3]/div[2]/div/div")
        time.sleep(5)
        keys_element(By.ID, "cardNum", card['number'])
        time.sleep(0.5)
        keys_element(By.ID, "cardHolder", card["name"])
        time.sleep(0.5)
        click_element(By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/div/div/div/div[3]/div[3]/div/span[1]/span[1]/span[1]/input")
        time.sleep(0.5)
        click_element(By.XPATH, f"/html/body/div[9]/div/div/div/ul/li[{str(int(card['expire_month']))}]")
        time.sleep(0.5)
        click_element(By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/div/div/div/div[3]/div[3]/div/span[3]/span[1]/span[1]/input")
        time.sleep(0.5)
        click_element(By.XPATH, f"/html/body/div[10]/div/div/div/ul/li[{str(int(card['expire_year'])-2024)}]")
        time.sleep(0.5)
        keys_element(By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/div/div/div/div[3]/div[4]/span/span[1]/input", card['cvc'])
        time.sleep(0.5)
        click_element(By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/div/div/div/div[4]/button")
        time.sleep(10)
        
        
    if address is not None:
        driver.get("https://www.aliexpress.com/p/address-manage/index.html")

        time.sleep(1.5)
        
        fake = Faker()
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        addr = address
        
        keys_element(driver, By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/form/div[2]/div[2]/div[1]/div[1]/div/div/span/input", first_name)
        time.sleep(0.5)
        keys_element(driver, By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/form/div[2]/div[2]/div[1]/div[2]/div/div/span/input", last_name)
        time.sleep(0.5)
        keys_element(driver, By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/form/div[2]/div[2]/div[1]/div[3]/div/div/span/span[2]/input", str(random.randint(1000000000,9999999999)))
        time.sleep(0.5)
        click_element(driver, By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/form/div[3]/div[2]/div[1]/div/div/div/span/span[1]/input")
        time.sleep(0.5)
        input_element = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/form/div[3]/div[2]/div[1]/div/div/div/span/span[1]/input")
        text_to_type = addr
        for char in text_to_type:
            input_element.send_keys(char)
            time.sleep(0.1)
        time.sleep(6)
        click_element(driver, By.XPATH, "/html/body/div[7]/div/ul/li[1]/div/span/div/div[2]")
        time.sleep(4)
        click_element(driver, By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/form/div[4]/div/div/div/div/div/div[1]/label/span[2]/span")
        time.sleep(1)
        click_element(driver, By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/form/div[5]/div/button[1]")
        time.sleep(10)
    
    if product is not None:
        driver.get(product)
        time.sleep(3)
        if color is not None:
            click_element(driver, By.XPATH, "/html/body/div[6]/div/div[1]/div/div[1]/div[1]/div[2]/div[8]/div/div/div[2]/div[2]/span[2]")
            click_element(driver, By.XPATH, f'//img[@alt="{color}"]')
            time.sleep(5)
            click_element(driver, By.XPATH, "/html/body/div[6]/div/div[1]/div/div[2]/div/div/div[7]/button[1]")
            
        input("Press Enter Once You Have Purchased The Product")
        driver.quit()
        
    input("Press Enter Once You Have Purchased The Product")
    driver.quit()

if __name__ == "__main__":
    options = { # SET ANY OF THESE TO `None` IF YOU DO NOT WANT THAT ARGUMENT TO BE USED.
        "region": "United Kingdom", # Optional, region of account, defaults to UK
        "address": "123 Aliexpress Lane", # Optional, address to be added to account automatically, set to None to not add an address
        "product": "https://www.aliexpress.com/item/1005007506962557.html", # Optional, Product to buy
        "color": "Water Blue", # Optional, Color of product to buy, if not set then product will not be bought automatically
        "email": None, # Optional, recommended to be left blank to generate random one. If not set to none then verification code will not be retrieved automatically.
        "password": None, # Optional, password to use, leave blank to generate random one.
        "proxy": { # Optional, set to None to not use a proxy.
            "ip": "1.1.1.1",
            "port": 1234,
            "username": "123",
            "password": "123"
        },
        "card": { # Optional, Card to be added automatically, Set to None to not add a card.
            "number": "1234123412341234",
            "name": "FIRSTNAME LASTNAME",
            "expire_month": "01",
            "expire_year": "2027",
            "cvc": "123"
        }
    }
    create_aliexpress_account(
        **options
    )
