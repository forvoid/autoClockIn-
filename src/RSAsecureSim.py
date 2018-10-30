#coding: UTF-8
#!/usr/bin/python

import unittest

from appium import webdriver
from time import sleep
import time
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.common.exceptions import NoSuchElementException

import unittest
import requests
import json

import hashlib

def md5sign(info):
    m = hashlib.md5()
    m.update(info.encode('utf-8'))
    return m.hexdigest()

class SecureSimTest(unittest.TestCase):

	
	def setUp(self):
		
		desired_caps = {}
		desired_caps['platformName'] = 'Android'
		desired_caps['platformVersion'] = '7.0'
		desired_caps['deviceName'] = 'cdf4c8580004'

	#	desired_caps['appPackage'] = 'com.xiaomi.moblie.lot'
	#	desired_caps['appActivity'] = 'com.xiaomi.moblie.lot.ui.TestCardActivity'

		desired_caps['appPackage'] = 'com.xiaomi.shop'
		desired_caps['appActivity'] = 'com.xiaomi.shop2.activity.MainActivity'

		# 开启appium的输入法
		desired_caps['unicodeKeyboard'] = 'True'
		desired_caps['resetKeyboard'] = 'True'

		self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
		
		
		self.appid = '100001'
		self.mid = '46011000000100000000'

	#	self.base = 'http://preview.secure.miot.10046.mi.com'
		self.base = 'http://secure.miot.10046.mi.com'
		self.proxies = {"http": "http://10.236.77.247:8888", "https": "http://10.236.77.247:8888", }
		self.now_time = 0
		self.localtime = 0
		self.target = open("status_record_0417.txt","w")

	
	def tearDown(self):
		# print "Done"
		self.driver.quit()
		self.target.close()
	

	def status(self):
		url = self.base + '/test/get_provision_status_info'
		params = {'mid':self.mid}


	#	r = requests.get(url, proxies=self.proxies, params=params)
		r = requests.get(url, params=params)

		all = r.json()
	#	print "all: ",all
		
		sort_keys = list(all.keys())
		sort_keys.sort()
	#	print "列表list(all.keys()): ",sort_keys
		keys_length = len(sort_keys)
		last = sort_keys[keys_length - 1]
	#	last = list(all.keys())[0]
		# print "最新的last: ",last
	#	print "last: ",last
		orderid = all.get(last).get('order_id')

		create_time = all.get(last).get('create_time')
		update_time = all.get(last).get('update_time')
		status = all.get(last).get('status')
		complete_time = update_time - create_time

	#	print "orderid: ",orderid
	#	print "complete_time: ",create_time,update_time,complete_time
		# print "status: ",status
		a = []
		a.append(orderid)
		a.append(complete_time)

		return a

	def spset(self, status, orderid):
		url = self.base + '/test/set_provision_status'
		
		info = '100001qzOaC+fOJNsJ4A8adgDIOb8jXh/ZlvvGY3RkPTnSSmk=&app_id=' + self.appid + '&mid=' + self.mid + '&order_id=' + orderid +'&status=' + status
		sign = md5sign(info)

		params = {'app_id':self.appid,'mid':self.mid,'status':status,'order_id':orderid,'sign':sign}
	#	r = requests.get(url, proxies=self.proxies, params=params)
		r = requests.get(url, params=params)
		# print r.text

	def should_provision(self):
		url = self.base + '/rsa_provision/should_provision'

		self.now_time = int(round(time.time() * 1000))
		self.localtime = time.asctime( time.localtime(time.time()) )


		info = '100001qzOaC+fOJNsJ4A8adgDIOb8jXh/ZlvvGY3RkPTnSSmk=&app_id=' + self.appid + '&mid=' + self.mid + '&timestamp=' + str(self.now_time)
		sign = md5sign(info)

		payload = {'app_id':self.appid,'mid':self.mid,'timestamp':self.now_time,'sign':sign}
		# print "payload: ",payload

		r = requests.get(url,params=payload)
		# print "should_provision Json: ",r.json()
		return r.json()


	def test_RSA_personal(self):

		
		self.driver.keyevent(3)
		sleep(3)
		
		self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.miui.home:id/cell_layout").childSelector(new UiSelector().index(0))').click()

		sleep(5)
		
		ConnectionError_num = 0

		for i in range(0,100):

			try:
				self.driver.implicitly_wait(30)
				self.driver.find_element_by_android_uiautomator('new UiSelector().text("检查状态")').click()
		
			except NoSuchElementException:
				self.driver.implicitly_wait(30)
				self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.miui.home:id/cell_layout").childSelector(new UiSelector().index(0))').click()
				self.driver.implicitly_wait(30)
				self.driver.find_element_by_android_uiautomator('new UiSelector().text("检查状态")').click()

			try:
				for j in range(0,10):
					sleep(6)
					
					self.driver.find_element_by_android_uiautomator('new UiSelector().text("CustomerApplication")').click()

			except NoSuchElementException:
				pass

		
			# print "=================第",i,"次"
			#
			#
			# print "2、调用should_provision："

			try:
				Json_should_provision = self.should_provision()

			except:
				# print "又出现ConnectionError"

				for i in range(0,10):
					try:
						Json_should_provision = self.should_provision()
					except:
						ConnectionError_num += 1
						# print "连接错误多少次：",ConnectionError_num



			
			status_10 = Json_should_provision['status']

			# print "3、调用get_provision_status_info："
			get_orderid_status = self.status()
			orderid = get_orderid_status[0]
			complete_time = get_orderid_status[1]

		#	print "这里",orderid,complete_time
			
			if status_10 != 10:
				# print "出错啦：",status_10
				
				# status_10是status,complete_time是完成个人化需要多长时间，localtime是年月日的时间，now_time是13位时间戳
				# Json_should_provision是should_provision接口返回结果
				self.target.write("%s status:%s\t%s\t%s\t%s\t%s\n"%(i,status_10,complete_time,self.localtime,self.now_time,Json_should_provision))
			else:
				self.target.write("%s status:%s\t%s\t%s\t%s\t%s\n"%(i,status_10,complete_time,self.localtime,self.now_time,Json_should_provision))
			

			# print "4、调用set_provision_status："
			self.spset('12', orderid)
			# print "重置状态后："
			self.status()
		
		# print "出错重试次数ConnectionError_num:",ConnectionError_num

	def test_qianming(self):
		sleep(10)

		self.driver.keyevent(3)
		sleep(3)
		
		self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.miui.home:id/cell_layout").childSelector(new UiSelector().index(1))').click()

		for i in range(0,50):
			self.driver.implicitly_wait(30)
			self.driver.find_element_by_android_uiautomator('new UiSelector().text("服务器签名卡验签")').click()

	def test_should_provision(self):
		self.should_provision()



if __name__ == "__main__":
#	unittest.main()
	suite = unittest.TestSuite()

# 查加解密时间的logcat命令
# adb logcat | grep -i "resp time"

# 	suite.addTest(SecureSimTest("test_RSA_personal"))
	suite.addTest(SecureSimTest("test_qianming"))
#	suite.addTest(SecureSimTest("test_should_provision"))
#	runner = unittest.TextTestRunner()
#	runner.run(suite)


	unittest.TextTestRunner(verbosity=2).run(suite)

