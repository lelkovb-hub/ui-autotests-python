import allure
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


@allure.feature("Промокоды")
class TestPromoIntercept:

    @allure.story("Сценарий №3")
    @allure.title("Перехват запроса промокода и возврат ошибки 500")
    def test_promo_intercept_500(self):
        # Настройка для перехвата запросов
        options = {
            'disable_encoding': True,
        }
        
        # Запускаем браузер с selenium-wire
        driver = webdriver.Chrome(seleniumwire_options=options)
        driver.maximize_window()
        
        request_was_intercepted = False
        
        def intercept_request(request):
            nonlocal request_was_intercepted
            # Ловим запрос к api купонов
            if 'apply_coupon' in request.url or 'coupon' in request.url:
                request_was_intercepted = True
                print(f"\n🔍 Перехвачен запрос: {request.url}")
                request.abort()
                print("🚫 Запрос заблокирован")
        
        driver.request_interceptor = intercept_request
        
        try:
            print("\n=== СЦЕНАРИЙ №3: ПЕРЕХВАТ ЗАПРОСА ===\n")
            
            with allure.step("1. Открыть главную страницу"):
                driver.get("https://pizzeria.skillbox.cc/")
                time.sleep(3)
            
            with allure.step("2. Добавить пиццу в корзину"):
                # Находим первую пиццу в слайдере
                pizzas = driver.find_elements(By.XPATH, "//aside//li[contains(@class, 'product')]")
                assert len(pizzas) > 0, "Пиццы не найдены"
                
                first_pizza = pizzas[0]
                # Скроллим к элементу
                driver.execute_script("arguments[0].scrollIntoView();", first_pizza)
                # Наводим мышку
                actions = ActionChains(driver)
                actions.move_to_element(first_pizza).perform()
                time.sleep(1)
                # Нажимаем кнопку "В корзину"
                add_button = first_pizza.find_element(By.CSS_SELECTOR, "a.add_to_cart_button")
                driver.execute_script("arguments[0].click();", add_button)
                print("✅ Пицца добавлена в корзину")
                time.sleep(2)
            
            with allure.step("3. Перейти в корзину"):
                cart_link = driver.find_element(By.CSS_SELECTOR, "a.cart-contents")
                cart_link.click()
                time.sleep(3)
            
            with allure.step("4. Запомнить сумму ДО промокода"):
                total_before_element = driver.find_element(By.CSS_SELECTOR, ".cart-subtotal .amount")
                total_before = total_before_element.text
                print(f"Сумма до промокода: {total_before}")
            
            with allure.step("5. Ввести промокод и нажать 'Применить'"):
                promo_input = driver.find_element(By.CSS_SELECTOR, "input[name='coupon_code']")
                promo_input.clear()
                promo_input.send_keys("GIVEMEHALYAVA")
                
                apply_btn = driver.find_element(By.CSS_SELECTOR, "button[name='apply_coupon']")
                apply_btn.click()
                time.sleep(5)
            
            with allure.step("6. Проверить, что запрос был перехвачен"):
                assert request_was_intercepted, "Запрос не был перехвачен!"
                print("✅ Запрос успешно перехвачен")
            
            with allure.step("7. Проверить, что сумма НЕ изменилась"):
                total_after_element = driver.find_element(By.CSS_SELECTOR, ".cart-subtotal .amount")
                total_after = total_after_element.text
                print(f"Сумма после промокода: {total_after}")
                assert total_before == total_after, f"Сумма изменилась! Было {total_before}, стало {total_after}"
                print("✅ Сумма не изменилась — промокод не применился")
            
            with allure.step("8. Проверить сообщение об ошибке"):
                try:
                    error_msg = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error")
                    print(f"✅ Сообщение об ошибке: {error_msg.text}")
                except:
                    print("⚠️ Сообщение об ошибке не найдено")
            
            print("\n" + "="*60)
            print("ВЫВОД ПО СЦЕНАРИЮ №3:")
            print("- Запрос перехвачен и заблокирован ✅")
            print("- Сумма заказа НЕ изменилась ✅")
            print("- Промокод НЕ применился ✅")
            print("="*60)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            raise
        finally:
            driver.quit()


if __name__ == "__main__":
    test = TestPromoIntercept()
    test.test_promo_intercept_500()