# Android environment
import unittest
import time
from appium import webdriver
from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.0'
desired_caps['deviceName'] = 'cdf4c8580004'

class SecureSimTest(unittest.TestCase):


    def text_setUp(self):
        print("开始时间",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '7.0'
        desired_caps['deviceName'] = 'cdf4c8580004'
        desired_caps['appPackage'] = 'com.xiaomi.shop'
        desired_caps['appActivity'] = 'com.xiaomi.shop2.activity.MainActivity'

        # 开启appium的输入法
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.keyevent(3)
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.miui.home:id/cell_layout").childSelector(new UiSelector().index(1))').click()
        sleep(1)
        try:
            self.driver.find_element_by_android_uiautomator('new UiSelector().text("首页")')

        except NoSuchElementException:
            self.login_unlock()
            print
            "没有进入首页"
        sleep(3)
        print("点击开始")
        self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.mi.oa:id/recyclerView").childSelector(new UiSelector().index(5))').click()
        print("点击结束")
        sleep(2)
        print("开始打卡")
        self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.mi.oa.app.gpscheck:id/check_in_Btn")').click()
        print("打卡结束")
        sleep(2)
        self.driver.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("com.mi.oa.app.gpscheck:id/positive_btn")').click()
        sleep(2)
        self.driver.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("com.mi.oa.app.gpscheck:id/host_titlebar_back")').click()

        self.driver.keyevent(3)
        print("退出 APP")
        print("结束时间", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    def tearDown(self):
        print("do something after test.Clean up.")

    def login_unlock(self):

        a = {
            "九宫格": "com.mi.oa:id/lock_pattern_view"
        }

        # unlock_text = self.driver.find_element_by_id(a["解锁提示"])
        lock_pattern = self.driver.find_element_by_id(a["九宫格"])
        x = lock_pattern.location.get('x')
        y = lock_pattern.location.get('y')
        width = lock_pattern.size.get('width')
        height = lock_pattern.size.get('height')
        print(x, y, width, height)
        offset = width / 6
        p11 = int(x + width / 6), int(y + height / 6)
        p12 = int(x + width / 2), int(y + height / 6)
        p13 = int(x + width - offset), int(y + height / 6)
        p21 = int(x + width / 6), int(y + height / 2)
        p22 = int(x + width / 2), int(y + height / 2)
        p23 = int(x + width - offset), int(y + height / 2)
        p31 = int(x + width / 6), int(y + height - offset)
        p32 = int(x + width / 2), int(y + height - offset)
        p33 = int(x + width - offset), int(y + height - offset)

        p3 = p13[0] - p11[0]
        TouchAction(self.driver)\
            .press(x=p11[0], y=p11[1])\
            .move_to(x=p12[0],y=p12[1]).wait(1000)\
            .move_to(x=p22[0],y=p22[1]).wait(1000)\
            .move_to(x=p32[0],y=p32[1]).wait(1000)\
            .move_to(x=p33[0], y=p33[1]).wait(1000).release().perform()
    # def daka(self):



if __name__ == "__main__":
#	unittest.main()
	suite = unittest.TestSuite()

# 查加解密时间的logcat命令
# adb logcat | grep -i "resp time"

# 	suite.addTest(SecureSimTest("test_RSA_personal"))
	suite.addTest(SecureSimTest("text_setUp"))
#	suite.addTest(SecureSimTest("test_should_provision"))
#	runner = unittest.TextTestRunner()
#	runner.run(suite)


	unittest.TextTestRunner(verbosity=1).run(suite)
