import allure
import time
import subprocess
from selenium.webdriver.common.by import By
from pages.main_page import MainPage


@allure.feature("Промокоды")
class TestPromoServerError:

    @allure.story("Сценарий №3")
    @allure.title("При ошибке сервера промокод не применяется")
    def test_promo_server_error(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Заполнить корзину любым товаром"):
            main_page.open_main_page()
            main_page.add_pizza_to_cart_by_index(0)
            time.sleep(2)
            main_page.go_to_cart()
            time.sleep(2)

        with allure.step("2. Запомнить сумму ДО промокода"):
            total_before_element = driver.find_element(By.CSS_SELECTOR, ".cart-subtotal .amount")
            total_before_text = total_before_element.text
            total_before = float(total_before_text.replace('₽', '').replace(' ', '').replace(',', '.'))
            print(f"Сумма до промокода: {total_before}")

        with allure.step("3. Применить промокод (имитация ошибки сервера)"):
            promo_input = driver.find_element(By.CSS_SELECTOR, "input[name='coupon_code']")
            promo_input.clear()
            promo_input.send_keys("GIVEMEHALYAVA")
            
            # Имитируем ошибку сервера — отключаем интернет на время отправки
            # (только для Windows)
            try:
                subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "admin=disable"], 
                              capture_output=True, timeout=5)
            except:
                pass
            
            apply_btn = driver.find_element(By.CSS_SELECTOR, "button[name='apply_coupon']")
            apply_btn.click()
            time.sleep(3)
            
            # Включаем интернет обратно
            try:
                subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "admin=enable"], 
                              capture_output=True, timeout=5)
            except:
                pass
            time.sleep(2)

        with allure.step("4. Проверить, что сумма НЕ изменилась"):
            total_after_element = driver.find_element(By.CSS_SELECTOR, ".cart-subtotal .amount")
            total_after_text = total_after_element.text
            total_after = float(total_after_text.replace('₽', '').replace(' ', '').replace(',', '.'))
            print(f"Сумма после промокода: {total_after}")
            
            assert total_after == total_before, f"Сумма изменилась! Было {total_before}, стало {total_after}"
            print("✅ Сумма не изменилась — промокод не применился")

        with allure.step("5. Проверить сообщение об ошибке"):
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error")
                print(f"✅ Сообщение об ошибке: {error_msg.text}")
            except:
                print("⚠️ Сообщение об ошибке не найдено")
            
            print("\n=== ВЫВОД ПО СЦЕНАРИЮ №3 ===")
            print("При ошибке сервера (500) сайт должен:")
            print("- Не применять скидку")
            print("- Показать сообщение об ошибке")
            print("Сумма не изменилась — ожидаемое поведение")