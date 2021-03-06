from selenium.webdriver.support.ui import WebDriverWait
from backend import Backend


class UPCBackend(Backend):

    def __init__(self, upc_mail, upc_user, upc_pass, ask_if_needed=True,
                 resolution=(1920, 1080), position=(0, 0)):
        super(UPCBackend, self).__init__(upc_mail, upc_pass, ask_if_needed, resolution, position)
        self.user = upc_user

    def __try_upc_login(self, driver):
        try:
            userbox = driver.find_element_by_id("edit-name")
            userbox.clear()
            userbox.send_keys(self.user)
            passbox = driver.find_element_by_id("edit-pass")
            passbox.clear()
            passbox.send_keys(self.passwd)
            driver.find_element_by_id("submit_ok").click()
            return True
        except:
            return False

    def join(self, meet_url):
        self.driver.get(meet_url)
        glogin_wait = WebDriverWait(self.driver, 20)
        glogin_wait.until(self._Backend__try_insert_mail)
        upc_wait = WebDriverWait(self.driver, 60)
        upc_wait.until(self.__try_upc_login)
        call_wait = WebDriverWait(self.driver, 20)
        call_wait.until(self._Backend__try_join_call)
