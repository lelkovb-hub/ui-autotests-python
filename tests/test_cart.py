import allure
import time
from selenium.webdriver.common.by import By
from pages.main_page import MainPage


@allure.feature("Корзина")
class TestCart:

    @allure.title("Проверка корзины")
    def test_cart(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.add_pizza_to_cart_by_index(0)
        time.sleep(2)
        main_page.go_to_cart()
        
        time.sleep(2)
        assert "cart" in driver.current_url, "Не в корзине"
        
        checkout_btn = driver.find_element(By.CSS_SELECTOR, ".checkout-button, a.checkout-button")
        assert checkout_btn.is_displayed(), "Нет кнопки оплаты"
        
        qty_input = driver.find_element(By.CSS_SELECTOR, "input.qty")
        qty_input.clear()
        qty_input.send_keys("2")
        
        update_btn = driver.find_element(By.CSS_SELECTOR, "button[name='update_cart']")
        update_btn.click()
        time.sleep(2)
        
        total = driver.find_element(By.CSS_SELECTOR, ".order-total .amount")
        assert total.text, "Сумма не отображается"
        print(f"Общая сумма: {total.text}")
        print("Тест корзины пройден")