from appium import webdriver
from time import sleep
desired_caps = {}
desired_caps['platformName'] = 'Android'  #appium会帮你识别
desired_caps['platformVersion'] = '7.0'
desired_caps['deviceName'] = 'cdf4c8580004'
 #deviceName你的模拟器名字，就是在下载AVD的时候，你填写的，忘了的回头去找，或者在模拟器顶部会显示
desired_caps['appPackage'] = 'com.miui.calculator' #计算器包
desired_caps['appActivity'] = '.cal.CalculatorActivity'

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

driver.find_element_by_name("1").click()

driver.find_element_by_name("5").click()

driver.find_element_by_name("9").click()

driver.find_element_by_name("9").click()

driver.find_element_by_name("5").click()

driver.find_element_by_name("+").click()

driver.find_element_by_name("6").click()

driver.find_element_by_name("=").click()
sleep(10)

# driver.quit()
