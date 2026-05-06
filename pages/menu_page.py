from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MenuPage(BasePage):
    URL = "https://pizzeria.skillbox.cc/menu/"
    
    # Локаторы
    DESSERTS_LINK = (By.XPATH, "//a[contains(text(),'Десерты')]")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".products .product")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".products .product .woocommerce-loop-product__title")

    def open_menu_page(self):
        self.open(self.URL)

    def select_desserts_category(self):
        """Нажимает на ссылку 'Десерты' в меню."""
        self.click(self.DESSERTS_LINK)
        # Ждём загрузки товаров
        self.wait.until(lambda d: len(d.find_elements(*self.PRODUCT_ITEMS)) > 0)

    def get_product_titles(self):
        """Возвращает список названий всех товаров на странице."""
        titles = self.driver.find_elements(*self.PRODUCT_TITLES)
        return [title.text.lower() for title in titles if title.text]

    def get_products_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_ITEMS))