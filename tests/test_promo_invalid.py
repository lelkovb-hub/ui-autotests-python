import allure
import time
from selenium.webdriver.common.by import By
from pages.main_page import MainPage


@allure.feature("Промокоды")
class TestPromoInvalid:

    @allure.story("Сценарий №2")
    @allure.title("Невалидный промокод DC120 не даёт скидку")
    def test_promo_code_invalid(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Заполнить корзину любым товаром"):
            main_page.open_main_page()
            main_page.add_pizza_to_cart_by_index(0)
            time.sleep(3)
            main_page.go_to_cart()
            time.sleep(3)

        with allure.step("2. Запомнить сумму ДО промокода"):
            total_before_element = driver.find_element(By.CSS_SELECTOR, ".cart-subtotal .amount")
            total_before_text = total_before_element.text
            total_before = float(total_before_text.replace('₽', '').replace(' ', '').replace(',', '.'))
            print(f"Сумма до: {total_before}")

        with allure.step("3. Применить невалидный промокод DC120"):
            promo_input = driver.find_element(By.CSS_SELECTOR, "input[name='coupon_code']")
            promo_input.clear()
            promo_input.send_keys("DC120")
            
            apply_btn = driver.find_element(By.CSS_SELECTOR, "button[name='apply_coupon']")
            apply_btn.click()
            time.sleep(3)

        with allure.step("4. Проверить сообщение об ошибке"):
            error_msg = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error")
            assert "Неверный купон" in error_msg.text
            print("✅ Сообщение об ошибке появилось")

        with allure.step("5. Проверить, что сумма НЕ изменилась"):
            total_after_element = driver.find_element(By.CSS_SELECTOR, ".cart-subtotal .amount")
            total_after_text = total_after_element.text
            total_after = float(total_after_text.replace('₽', '').replace(' ', '').replace(',', '.'))
            
            assert total_after == total_before, f"Сумма изменилась!"
            print(f"✅ Сумма не изменилась: {total_before}")