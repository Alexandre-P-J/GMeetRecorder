from selenium.webdriver.support.ui import WebDriverWait
from backend import Backend


class UCABackend(Backend):

    def __init__(self, uca_mail, uca_user, uca_pass, ask_if_needed=True,
                 resolution=(1920, 1080), position=(0, 0)):
        super(UCABackend, self).__init__(uca_mail, uca_pass, ask_if_needed, resolution, position)
        self.user = uca_user

    def __try_uca_login(self, driver):
        try:
            userbox = driver.find_element_by_id("username")
            userbox.clear()
            userbox.send_keys(self.user)
            passbox = driver.find_element_by_id("password")
            passbox.clear()
            passbox.send_keys(self.passwd)
            driver.find_element_by_css_selector("#regularsubmit > button").click()
            return True
        except:
            return False

    def join(self, meet_url):
        self.driver.get(meet_url)
        glogin_wait = WebDriverWait(self.driver, 20)
        glogin_wait.until(self._Backend__try_insert_mail)
        uca_wait = WebDriverWait(self.driver, 60)
        uca_wait.until(self.__try_uca_login)
        call_wait = WebDriverWait(self.driver, 20)
        call_wait.until(self._Backend__try_join_call)
