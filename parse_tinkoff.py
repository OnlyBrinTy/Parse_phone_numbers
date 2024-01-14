from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from itertools import groupby, cycle

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
options = Options()


links = {'web_page': 'https://www.tinkoff.ru/mobile-operator/numbers/',
         'button': '//*[@id="form"]/div[1]/div/div/div/div[1]/div/div/form/div[2]/div/div/div[3]/div/div/label[1]',
         'input': '/html/body/div[1]/div/div[5]/div/div[1]/div/div/div/div[1]/div/div/form/'
                  'div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div/input',
         'number': '/html/body/div[1]/div/div[5]/div/div[1]/div/div/div/div[1]'
                   '/div/div/form/div[2]/div/div/div[4]/label[1]/div[1]/div'}
with open('IPs.txt', 'r') as inp_file:
    IPs = cycle(inp_file.read().split('\n'))


def change_ip(ip):
    global driver
    options.add_argument(f'--proxy-server={ip}')
    driver = webdriver.Chrome(service=s, chrome_options=options)


def main():
    while True:
        try:
            driver.get(links['web_page'])
            driver.find_element(By.XPATH, links['button']).click()
            input_field = driver.find_element(By.XPATH, links['input'])
        except Exception:
            change_ip(next(IPs))
        else:
            break

    key_numbers = ((3, 1000), (5, 1000))
    previous_n2 = 0
    exceptions_in_row = 0
    for key, start in key_numbers:
        for n1, n2, n3, n4 in map(str, range(start, 10000)):
            if n2 != previous_n2:
                print(key, n1, n2)
            previous_n2 = n2

            try:
                input_field.send_keys(Keys.BACK_SPACE * 7)
                input_field.send_keys(f'{n1}{n2}{key}{n3}{key}{n4}{key}')
                number = WebDriverWait(driver, 0.5).until(
                    ec.presence_of_element_located((By.XPATH, links['number']))).text
            except Exception:
                exceptions_in_row += 1
                if exceptions_in_row >= 10:
                    change_ip(next(IPs))

                continue

            exceptions_in_row = 0
            if number[14] == number[17]:
                with open('good_numbers.txt', 'a') as output_file:
                    print(number, file=output_file)


if __name__ == '__main__':
    main()
