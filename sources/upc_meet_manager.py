from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


class UPCMeetManager():
    join_now_buttons = [
        "Uneix-me ara",
        "Unirse ahora",
        "Join now",
    ]
    ask_join_buttons = [
        "Sol·licita unir",  # incomplete match is valid
        "Solicitar unirse",
        "Ask to join"
    ]

    def __init__(self, upc_mail, upc_user, upc_pass, ask_if_needed=True,
                 resolution=(1920, 1080), position=(0, 0)):
        self.mail = upc_mail
        self.user = upc_user
        self.passwd = upc_pass
        if ask_if_needed:
            self.allowed_join_buttons = self.join_now_buttons + self.ask_join_buttons
        else:
            self.allowed_join_buttons = self.join_now_buttons
        self.resolution = resolution
        self.position = position

    def __init_driver(self):
        options = Options()
        options.headless = False
        options.add_argument("-kiosk")
        options.set_preference("permissions.default.microphone", 2)
        options.set_preference("permissions.default.camera", 2)
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0")

        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webnotifications.enabled", False)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()

        desired = webdriver.DesiredCapabilities.FIREFOX

        driver = webdriver.Firefox(firefox_profile=profile, options=options,
                                   desired_capabilities=desired,
                                   executable_path="/usr/local/bin/geckodriver")
        driver.set_window_position(*(self.position))
        driver.set_window_size(*(self.resolution))
        time.sleep(1)
        return driver

    def __try_glogin(self, driver):
        try:
            driver.find_element_by_id("identifierId").send_keys(self.mail)
            driver.find_element_by_id("identifierNext").click()
            return True
        except:
            return False

    def __try_upc_login(self, driver):
        try:
            driver.find_element_by_id("edit-name").send_keys(self.user)
            driver.find_element_by_id("edit-pass").send_keys(self.passwd)
            driver.find_element_by_id("submit_ok").click()
            return True
        except:
            return False

    def __try_join_call(self, driver):
        btexts = [
            f"contains(text(), '{i}')" for i in self.allowed_join_buttons]
        xpath = f"//span[{' or '.join(btexts)}]"
        try:
            match = driver.find_element(By.XPATH, xpath)
            match.click()
            return True
        except:
            return False

    def get_num_people(self, fallback=-1):
        try:
            return int(self.driver.find_element_by_class_name("wnPUne.N0PJ8e").text)
        except:
            return fallback

    def __join(self, meet_url):
        self.driver.get(meet_url)
        glogin_wait = WebDriverWait(self.driver, 20)
        glogin_wait.until(self.__try_glogin)
        upc_wait = WebDriverWait(self.driver, 20)
        upc_wait.until(self.__try_upc_login)
        call_wait = WebDriverWait(self.driver, 20)
        call_wait.until(self.__try_join_call)

    def meet_while(self, meet_url, min_seconds, max_seconds, fraction_ppl_left):
        self.driver = self.__init_driver()
        self.__join(meet_url)
        current_time = time.time()
        current_ppl = self.get_num_people(fallback=-1)
        soft_end = current_time + min_seconds
        hard_end = current_time + max_seconds
        max_ppl = 0
        while (hard_end - current_time) > 0 and not ((soft_end - current_time) <= 0 and current_ppl <= (max_ppl * (1 - fraction_ppl_left))):
            time.sleep(5)
            max_ppl = max(max_ppl, current_ppl)
            current_ppl = self.get_num_people(fallback=-1)
            current_time = time.time()
        self.driver.close()
