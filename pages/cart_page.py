from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    # Локаторы на основе скрина
    CART_TABLE = (By.CSS_SELECTOR, "table.shop_table")
    CART_ITEMS = (By.CSS_SELECTOR, "tr.cart_item, .cart_item")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-name a")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-price .amount")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input.qty")
    PRODUCT_SUBTOTAL = (By.CSS_SELECTOR, ".product-subtotal .amount")
    REMOVE_ITEM_BTN = (By.CSS_SELECTOR, "a.remove")
    UPDATE_CART_BTN = (By.CSS_SELECTOR, "button[name='update_cart']")
    
    # Блок с суммой
    CART_TOTAL = (By.CSS_SELECTOR, ".cart_totals")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".order-total .amount, .cart-subtotal .amount")
    CHECKOUT_BTN = (By.CSS_SELECTOR, ".checkout-button, a.checkout-button")

    def get_cart_items_count(self):
        """Возвращает количество товаров в корзине."""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)

    def get_product_names(self):
        """Возвращает список названий товаров в корзине."""
        names = self.driver.find_elements(*self.PRODUCT_NAME)
        return [name.text for name in names]

    def update_quantity(self, item_index, quantity):
        """Изменяет количество товара по индексу (начиная с 0)."""
        quantity_inputs = self.driver.find_elements(*self.QUANTITY_INPUT)
        if item_index < len(quantity_inputs):
            qty_input = quantity_inputs[item_index]
            qty_input.clear()
            qty_input.send_keys(str(quantity))
            self.click(self.UPDATE_CART_BTN)
            return True
        return False

    def remove_item(self, item_index):
        """Удаляет товар из корзины по индексу."""
        remove_btns = self.driver.find_elements(*self.REMOVE_ITEM_BTN)
        if item_index < len(remove_btns):
            remove_btns[item_index].click()
            return True
        return False

    def get_total_price(self):
        """Возвращает общую сумму заказа."""
        return self.get_text(self.TOTAL_PRICE)

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN)