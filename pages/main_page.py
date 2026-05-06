from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage


class MainPage(BasePage):
    URL = "https://pizzeria.skillbox.cc/"

    # Локаторы на основе твоего XPath
    SLIDER_AREA = (By.XPATH, "//aside")
    PIZZA_ITEMS = (By.XPATH, "//aside//li[contains(@class, 'product')]")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "a.add_to_cart_button")
    CART_LINK = (By.CSS_SELECTOR, "a.cart-contents")

    def open_main_page(self):
        self.open(self.URL)

    def get_slider_pizzas(self):
        """Возвращает список пицц в слайдере."""
        # Ждём загрузки слайдера
        self.wait.until(lambda d: len(d.find_elements(*self.PIZZA_ITEMS)) > 0)
        return self.driver.find_elements(*self.PIZZA_ITEMS)

    def add_pizza_to_cart_by_index(self, index):
        """Добавляет пиццу в корзину по индексу."""
        pizzas = self.get_slider_pizzas()
        if index < len(pizzas):
            pizza = pizzas[index]
            # Скроллим к элементу
            self.driver.execute_script("arguments[0].scrollIntoView();", pizza)
            # Наводим мышку
            actions = ActionChains(self.driver)
            actions.move_to_element(pizza).perform()
            # Находим кнопку добавления
            try:
                add_button = pizza.find_element(*self.ADD_TO_CART_BTN)
                add_button.click()
                return True
            except:
                return False
        return False

    def go_to_cart(self):
        self.click(self.CART_LINK)