# Android environment
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from eyes import Eyes

DESIRED_CAPS = dict(
    avd='Pixel_4_API_31',
    platformName='Android',
    deviceName='Pixel_2_API_31',
    appPackage='com.globe.gcash.android',
    appActivity='gcash.module.splashscreen.mvp.view.SplashScreenActivity',
    noReset=True
)
APPIUM_URL = 'http://localhost:4723/wd/hub'
PIN_ELEMENT_ID = 'com.globe.gcash.android:id/mpin'
SERVICES_ITEM_ID = 'com.globe.gcash.android:id/tvItemLabel'

class Bot:
    def __init__(self):
        self.driver = webdriver.Remote(APPIUM_URL, DESIRED_CAPS)
        self._eyes = Eyes()
        
    def start(self):
        self._services = []
        self.driver.implicitly_wait(5)
    
    def stop(self):
        self.driver.close_app()

    def login(self, pin):
        pin_element = self.driver.find_element_by_id(PIN_ELEMENT_ID)
        pin_element.send_keys(pin)
    
    def open_service(self, service):
        label_elements = self.driver.find_elements_by_id(SERVICES_ITEM_ID)
        for label_element in label_elements:
            if label_element.text == service:
                label_element.click()
                return
    
    def open_gforest(self):
        self.open_service('GForest')

    def open_leaderboard(self):
        view_all_friends_ui_selector = 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains("View All Friends"))'
        view_all_friends = self.driver.find_element_by_android_uiautomator(view_all_friends_ui_selector)
        view_all_friends.click()
    
    def visit(self, name):
        friend_ui_selector = 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains("' + name + '"))'
        friend = self.driver.find_element_by_android_uiautomator(friend_ui_selector)
        friend.click()

    def find_energy(self):
        time.sleep(5)
        screenshot_base64 = self.driver.get_screenshot_as_base64()
        return self._eyes.find_bubbles(screenshot_base64)
    
    def save_screenshot(self, filename):
        time.sleep(5)
        self.driver.save_screenshot(filename)

    def collect_energy(self, bubble):
        (x, y), _, _ = bubble
        TouchAction(self.driver).press(None, x, y).release().perform()