import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

url = r'https://www.myetherwallet.com/#send-transaction'
driver_path = r'C:\Users\vdanh\Desktop\python\webdriver\Window\chromedriver.exe'
xpath_btn_radio = r'/html/body/section[1]/div/main/article[1]/div[2]/wallet-decrypt-drtv/article/section[1]/label[7]/span'
xpath_btn_unlock = r'//*[@id="selectedTypeKey"]/div[4]/a'
xpath_btn_expand = r'/html/body/section[1]/div/main/article[1]/div[1]/a'
xpath_btn_all_balance = r'/html/body/section[1]/div/main/article[2]/div/article[2]/section[1]/p/a'
xpath_text_all_balance = r'/html/body/section[1]/div/main/article[2]/div/article[2]/section[1]/div[2]/div/input'
id_text_area = r'aria6'
privatekey = 'caf74f1c3ae6ba91e988f73e0d50187b4c58527a4b58d3131d9d64e675a990fa'
pk_len = 64
hex_list = list('0123456789abcdef')
driver = webdriver.Chrome(driver_path)


def waiting(locator, message, time=30):
    try:
        WebDriverWait(driver, time).until(EC.presence_of_element_located(locator))
    finally:
        print("founded: {}".format(message))


def gen_pk() -> str():
    len = pk_len
    privatekey = str()
    while len > 0:
        privatekey += hex_list[random.randint(0, 15)]
        len -= 1
    return privatekey


def main():
    driver.get(url)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    waiting((By.ID, id_text_area), message='text area')
    text_area = driver.find_element_by_id(id_text_area)  # text area to input private key
    text_area.send_keys(privatekey)

    waiting((By.XPATH, xpath_btn_unlock), message='unlock btn')
    btn_unlock = driver.find_element_by_xpath(xpath_btn_unlock)  # btn to unlock wallet
    btn_unlock.click()

    # getting account's currency
    # eth = driver.find_element_by_xpath(
    #     '/html/body/section[1]/div/main/article[2]/section/wallet-balance-drtv/aside/div[1]/ul[2]/li/span')
    # print(eth.text)

    text_all_balance = driver.find_element_by_xpath(xpath_text_all_balance)
    text_all_balance.clear()
    print('"{}"'.format(text_all_balance.get_attribute('value')))

    waiting((By.XPATH, xpath_btn_all_balance), message='all balance btn')
    btn_all_balance = driver.find_element_by_xpath(xpath_btn_all_balance)
    btn_all_balance.click()

    balance = text_all_balance.get_attribute('value')
    while balance == '':
        balance = text_all_balance.get_attribute('value')
    print(balance)

    waiting((By.XPATH, xpath_btn_expand), message='expand btn')
    btn_expand = driver.find_element_by_xpath(xpath_btn_expand)  # btn to expand the menu again
    btn_expand.click()

    while True:
        pk = gen_pk()
        text_area.clear()
        text_area.send_keys(pk)
        btn_unlock.click()
        text_all_balance.clear()
        # print('"{}"'.format(text_all_balance.get_attribute('value')))
        btn_all_balance.click()
        balance = text_all_balance.get_attribute('value')
        while balance == '':
            balance = text_all_balance.get_attribute('value')
        print('{} {}'.format(pk, balance))
        btn_expand.click()

    # soup = BeautifulSoup(eth.get_attribute('innerHTML'), 'html.parser')
    # while True:
    #     f = soup.find('ul', {'class': 'account-info point'}).find('li', {'class': 'ng-binding'}).find('span', {
    #         'class': 'mono wrap ng-binding'})
    #     print(f)

    # waiting((By.XPATH, xpath_btn_expand), message='expand btn')
    # btn_expand = driver.find_element_by_xpath(xpath_btn_expand)  # btn to expand the menu again
    # btn_expand.click()
    #
    # waiting((By.ID, id_text_area), message='text area')
    # text_area.clear()
    # text_area.send_keys(privatekey1)
    # waiting((By.XPATH, xpath_btn_unlock), message='unlock btn')
    # btn_unlock.click()


if __name__ == '__main__':
    main()
