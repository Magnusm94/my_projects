import time

import pandas as pd
from selenium import webdriver, common


class selenium:
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(executable_path=
                               '/Users/magnusmarvik/PycharmProjects/lilleslott_backend/tools/tripletex/chromedriver',
                               options=options)
    username = ''
    passord = ''

    def login(self):
        self.browser.get('https://tripletex.no/execute/login?site=no')
        while True:
            try:
                self.browser.find_element_by_xpath('/html/body/div/div/div[2]/form/div[1]/div/div[1]/input').send_keys(
                    self.username)
                self.browser.find_element_by_xpath('/html/body/div/div/div[2]/form/div[1]/div/div[2]/input').send_keys(
                    self.passord)
                break
            except TypeError:
                pass
        self.browser.find_element_by_xpath('/html/body/div/div/div[2]/form/div[1]/div/input[5]').click()

    def unpaid_sent_bills(self):
        self.browser.get('https://tripletex.no/execute/listInvoices?contextId=4223892')
        while True:
            try:
                self.browser.find_element_by_xpath(
                    '/html/body/div[1]/div/main/div[2]/div[5]/div[2]/div[2]/form/table/tbody/tr[1]/td[3]/div/a')
                self.browser.find_element_by_xpath(
                    '/html/body/div[1]/div/main/div[2]/div[5]/div[2]/div[1]/form[2]/div/div[7]/button').click()
                time.sleep(3)
                self.browser.find_element_by_xpath(
                    '/html/body/div[1]/div/main/div[2]/div[5]/div[2]/div[1]/form[2]/div/div[6]/fieldset[3]/div[7]/label/span').click()
                time.sleep(3)
                break
            except common.exceptions.NoSuchElementException:
                pass
        while True:
            try:
                table = self.browser.find_element_by_xpath(
                    '/html/body/div[1]/div/main/div[2]/div[5]/div[2]/div[2]/form/table')
                break
            except common.exceptions.NoSuchElementException:
                pass
        file = open('test.txt', 'w')
        file.write(table.text)
        file.close()
        readhtml = pd.read_html(self.browser.page_source)
        print(readhtml)
        df = pd.DataFrame(data=readhtml)
        self.browser.close()
        return df


tripletex = selenium()
tripletex.login()
print(tripletex.unpaid_sent_bills())
