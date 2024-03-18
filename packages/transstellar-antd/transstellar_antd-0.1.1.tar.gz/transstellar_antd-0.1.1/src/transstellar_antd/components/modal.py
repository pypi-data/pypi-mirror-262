from urllib.parse import urlparse

from transstellar.framework import Element


class Modal(Element):
    XPATH_CURRENT = '//div[contains(@class, "ant-modal")]'

    XPATH_CLOSE_BUTTON = '//button[contains(@class, "ant-modal-close")]'

    def close(self):
        close_button = self.find_dom_element_by_xpath(self.XPATH_CLOSE_BUTTON)
        close_button.click()

        self.wait_for_dom_element_to_disappear_by_xpath(self.XPATH_CLOSE_BUTTON)
