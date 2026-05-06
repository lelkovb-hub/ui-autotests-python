from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        logger.info(f"Открытие страницы: {url}")
        self.driver.get(url)

    def click(self, locator):
        logger.info(f"Клик по элементу: {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def input_text(self, locator, text):
        logger.info(f"Ввод текста '{text}' в поле: {locator}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text