from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from abc import ABC, abstractmethod
import time


class Backend(ABC):
    # string matching may be more reliable than js generated classes/xpath/ids...
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

    def __init__(self, mail, passwd, ask_if_needed=True,
                 resolution=(1920, 1080), position=(0, 0)):
        self.mail = mail
        self.passwd = passwd
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

    def __try_insert_mail(self, driver):
        try:
            signbutton = driver.find_element_by_class_name(
                "NPEfkd.RveJvd.snByac")
            signbutton.click()
            time.sleep(1)  # not required
        except:
            pass
        try:
            userbox = driver.find_element_by_id("identifierId")
            userbox.clear()
            userbox.send_keys(self.mail)
            driver.find_element_by_id("identifierNext").click()
            return True
        except:
            return False

    def __try_join_call(self, driver):
        btexts = [
            f"contains(text(), '{i}')" for i in self.allowed_join_buttons]
        xpath = f"//span[{' or '.join(btexts)}]"
        try:
            match = driver.find_element_by_xpath(xpath)
            match.click()
            return True
        except:
            return False

    @abstractmethod
    def join(self, meet_url):
        pass

    def exit(self):
        try:
            self.driver.find_element_by_class_name(
                "DPvwYc.JnDFsc.grFr5.FbBiwc").click()
            time.sleep(5)
        except:
            pass
        self.driver.quit()

    def get_num_people(self):
        try:
            ppl = self.driver.find_element_by_class_name("wnPUne.N0PJ8e").text
            return int(ppl)
        except:
            return -1

    def __invalid_driver(self):
        try:
            self.driver.title
            return False
        except:
            return True

    def __reconnect(self, meet_url, force, times=3):
        for _ in range(times):
            invalid = self.__invalid_driver()
            if (not (force or invalid)):
                return True
            elif (not invalid):
                self.driver.quit()
            try:
                self.driver = self.__init_driver()
                self.join(meet_url)
                return True
            except:
                force = True
        return False

    def meet_while(self, meet_url, min_seconds, max_seconds, fraction_ppl_left):
        if (not self.__reconnect(meet_url, True)):
            return
        current_time = time.time()
        current_ppl = self.get_num_people()
        soft_end = current_time + min_seconds
        hard_end = current_time + max_seconds
        max_ppl = 0
        while (hard_end - current_time) > 0 and not ((soft_end - current_time) <= 0 and current_ppl <= (max_ppl * (1 - fraction_ppl_left))):
            if (not self.__reconnect(meet_url, False)):
                break
            max_ppl = max(max_ppl, current_ppl)
            tmp = self.get_num_people()
            current_ppl = tmp if tmp != -1 else current_ppl
            current_time = time.time()
            time.sleep(1)
        self.exit()
