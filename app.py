from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui, sys

options = Options()
options.headless = True
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
options.add_argument("--lang=pt-BR,pt")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36', "acceptLanguage": "pt-BR,pt"})

try:
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
    username_field = driver.find_element(By.XPATH, '//input[@name="username"]')
    ActionChains(driver).move_to_element(username_field).click().perform()
    pyautogui.typewrite("seyzalel", interval=0.2)

    password_field = driver.find_element(By.XPATH, '//input[@name="password"]')
    ActionChains(driver).move_to_element(password_field).click().perform()
    pyautogui.typewrite("Sey17zalel17@$", interval=0.2)

    entrar_button_xpath = '//div[contains(@class, "x9f619") and contains(text(), "Entrar")]'
    entrar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, entrar_button_xpath)))
    ActionChains(driver).move_to_element(entrar_button).click().perform()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[contains(@alt, "Foto do perfil de seyzalel")]')))
    print("Login bem sucedido.")
except Exception as e:
    print("Login mal sucedido.", e)
    sys.exit(1)