from selenium import webdriver
# from selenium.webdriver.common.keys import keys

driver = webdriver.Firefox()
driver.get('http://www.python.org')
# assert 'python' in driver.title
# elem = driver.find_element_by_name('q')