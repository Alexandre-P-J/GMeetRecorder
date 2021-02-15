from selenium.webdriver.support.ui import WebDriverWait
from backend import Backend


class GmailBackend(Backend):

    def __init__(self, mail, passwd, ask_if_needed=True,
                 resolution=(1920, 1080), position=(0, 0)):
        super(GmailBackend, self).__init__(mail, passwd, ask_if_needed, resolution, position)

    def __try_insert_passwd(self, driver):
        try:
            passbox = driver.find_element_by_xpath('//*[@id ="password"]/div[1]/div / div[1]/input') 
            passbox.clear()
            passbox.send_keys(self.passwd) 
            driver.find_element_by_id("passwordNext").click()
            return True
        except:
            return False

    def join(self, meet_url):
        self.driver.get(meet_url)
        mail_wait = WebDriverWait(self.driver, 20)
        mail_wait.until(self._Backend__try_insert_mail)
        pass_wait = WebDriverWait(self.driver, 60)
        pass_wait.until(self.__try_insert_passwd)
        call_wait = WebDriverWait(self.driver, 20)
        call_wait.until(self._Backend__try_join_call)
