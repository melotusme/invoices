from selenium import webdriver

browser = webdriver.Firefox()
url = "http://ruby.zhirong.info/"
browser.get(url)

loginBtn = browser.find_element_by_xpath('//a[@href="/login"]')
loginBtn.click()


usernameInput = browser.find_element_by_id("user_username")
user_password.send_keys("wrong")
passwordInput = browser.find_element_by_id("user_password")
passwordInput.send_keys("")
passwordInput.submit()
