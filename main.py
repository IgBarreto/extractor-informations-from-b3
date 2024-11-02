import importlib
from time import sleep

# from plyer import notification
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

# import constants
# import pandas as pd


CONSTANTS = {
    'URL': 'https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm',  # noqa
    'REPORT_FLOWS': [
        'Balanço Patrimonial Ativo',
        'Balanço Patrimonial Passivo',
        'Demonstração do Resultado',
    ],
    'DRE_REPORT_CATEGORICAL_COLUMNS': ['Conta', 'Descrição'],
}


def get_driver(browser_name='Edge', headless=True):
    if browser_name.lower() == "chrome":
        ChromeService = importlib.import_module(
            "selenium.webdriver.chrome.service"
        ).Service
        ChromeOptions = importlib.import_module(
            "selenium.webdriver.chrome.options"
        ).Options
        service = ChromeService()
        options = ChromeOptions()
        options.headless = headless
        driver = importlib.import_module("selenium.webdriver").Chrome(
            service=service, options=options
        )

    elif browser_name.lower() == "firefox":
        FirefoxService = importlib.import_module(
            "selenium.webdriver.firefox.service"
        ).Service
        FirefoxOptions = importlib.import_module(
            "selenium.webdriver.firefox.options"
        ).Options
        service = FirefoxService()
        options = FirefoxOptions()
        options.headless = headless
        driver = importlib.import_module("selenium.webdriver").Firefox(
            service=service, options=options
        )

    elif browser_name.lower() == "edge":
        EdgeService = importlib.import_module(
            "selenium.webdriver.edge.service"
        ).Service
        EdgeOptions = importlib.import_module(
            "selenium.webdriver.edge.options"
        ).Options
        service = EdgeService()
        options = EdgeOptions()
        options.headless = headless
        driver = importlib.import_module("selenium.webdriver").Edge(
            service=service, options=options
        )

    else:
        raise ValueError(
            "Navegador não suportado. Escolha 'chrome', 'firefox' ou 'edge'."
        )

    return driver


def click_element(wait, driver, element_type, element_name):
    try:
        element = wait.until(
            EC.element_to_be_clickable((element_type, element_name))
        )
        element.click()
    except ElementClickInterceptedException:
        print(f"Trying to click on the button {element} again")
        driver.execute_script("arguments[0].click()", element)


def select_element(wait, element_type, element_name, element_value):
    element = wait.until(
        EC.presence_of_element_located((element_type, element_name))
    )
    select = Select(element)
    select.select_by_visible_text(element_value)


def get_banks():
    driver = get_driver()
    driver.implicitly_wait(10)
    driver.get(CONSTANTS.get('URL'))
    wait = WebDriverWait(driver, 10)
    iframe = driver.find_element(By.ID, 'bvmf_iframe')
    driver.switch_to.frame(iframe)

    click_element(
        wait, driver, By.CSS_SELECTOR, '[href="#accordionClassification" ]'
    )
    select_element(
        wait, By.CSS_SELECTOR, '[formcontrolname="selectSector"]', 'Financeiro'
    )
    click_element(wait, driver, By.LINK_TEXT, 'Bancos')
    select_element(
        wait, By.CSS_SELECTOR, '[formcontrolname="selectPage"]', '120'
    )
    sleep(1)
    banks = driver.find_elements(By.CLASS_NAME, 'card-body')
    list_banks = []
    for bank in banks:
        bank_short_name = bank.find_element(By.TAG_NAME, 'h5').text
        bank_name = bank.find_element(By.CLASS_NAME, 'card-text').text
        list_banks.append([bank_short_name, bank_name])
    return [list_banks, [driver, wait]]


if __name__ == '__main__':
    banks = get_banks()[0]
    print(banks)
