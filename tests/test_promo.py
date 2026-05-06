import allure
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage


@allure.feature("Промокоды")
class TestPromo:

    @allure.story("Сценарий №1")
    @allure.title("Применение промокода GIVEMEHALYAVA даёт скидку 10%")
    def test_promo_code_givemehalyava(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Заполнить корзину любым товаром"):
            main_page.open_main_page()
            main_page.add_pizza_to_cart_by_index(0)
            time.sleep(3)
            main_page.go_to_cart()
            time.sleep(3)

        with allure.step("2. Запомнить общую сумму ДО промокода"):
            total_before_element = driver.find_element(By.CSS_SELECTOR, ".cart-subtotal .amount")
            total_before_text = total_before_element.text
            total_before = float(total_before_text.replace('₽', '').replace(' ', '').replace(',', '.'))
            print(f"Сумма до промокода: {total_before}")

        with allure.step("3. Применить промокод GIVEMEHALYAVA"):
            promo_input = driver.find_element(By.CSS_SELECTOR, "input[name='coupon_code']")
            promo_input.clear()
            promo_input.send_keys("GIVEMEHALYAVA")
            
            apply_btn = driver.find_element(By.CSS_SELECTOR, "button[name='apply_coupon']")
            apply_btn.click()
            time.sleep(5)

        with allure.step("4. Проверить, что появилось сообщение об успешном применении"):
            success_msg = driver.find_element(By.CSS_SELECTOR, ".woocommerce-message")
            assert "Coupon code applied successfully" in success_msg.text or "применён" in success_msg.text
            print("✅ Сообщение появилось")

        with allure.step("5. Проверить, что появилась строка с купоном"):
            coupon_line = driver.find_element(By.CSS_SELECTOR, ".cart-discount")
            assert "GIVEME" in coupon_line.text
            print("✅ Строка с купоном появилась")

        with allure.step("6. Проверить финальную сумму"):
            total_after_element = driver.find_element(By.CSS_SELECTOR, ".order-total .amount")
            total_after_text = total_after_element.text
            total_after = float(total_after_text.replace('₽', '').replace(' ', '').replace(',', '.'))
            
            expected_after = round(total_before * 0.9, 2)
            assert abs(total_after - expected_after) < 1, f"Скидка не 10%! Было {total_before}, стало {total_after}"
            
            print(f"✅ Промокод работает: {total_before} -> {total_after}")