import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.auth_page import AuthPage


@allure.feature("Промокоды")
class TestPromoOnce:

    TEST_USERNAME = "testbo"
    TEST_PASSWORD = "12345678"

    # --- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ (БОЛЕЕ НАДЕЖНЫЕ) ---
    def clear_cart(self, driver):
        """Очищает корзину."""
        driver.get("https://pizzeria.skillbox.cc/cart/")
        time.sleep(2)
        # Удаляем все товары, если они есть
        while True:
            remove_buttons = driver.find_elements(By.CSS_SELECTOR, ".remove")
            if not remove_buttons:
                break
            for btn in remove_buttons:
                try:
                    btn.click()
                    time.sleep(1)
                    # Обработка всплывающего окна подтверждения, если оно есть
                    try:
                        alert = driver.switch_to.alert
                        alert.accept()
                        time.sleep(1)
                    except:
                        pass
                except:
                    pass
        print("✅ Корзина очищена")

    def add_items_to_cart(self, driver, main_page):
        """Добавляет товары в корзину, используя более надежные методы."""
        # 1. Добавляем первую пиццу на главной странице
        main_page.open_main_page()
        time.sleep(2)
        main_page.add_pizza_to_cart_by_index(0)
        time.sleep(2)

        # 2. Добавляем вторую пиццу на главной странице
        main_page.add_pizza_to_cart_by_index(1)
        time.sleep(2)

        # 3. Добавляем напиток через переход в каталог "Меню" -> "Напитки"
        print("Добавляем напиток...")
        driver.get("https://pizzeria.skillbox.cc/menu/")
        time.sleep(2)

        # Находим и кликаем по категории "Напитки" (если есть выпадающий список или секция)
        try:
            # Пробуем найти ссылку на категорию напитков
            drinks_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Напитки')]"))
            )
            drinks_link.click()
            time.sleep(2)
        except:
            print("Не удалось перейти по ссылке 'Напитки', ищем товары на странице...")

        # Теперь на странице меню (или категории напитков) ищем кнопку "В корзину" у первого попавшегося товара
        # Ждем, пока загрузятся товары
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product"))
        )
        
        # Находим первую кнопку "В корзину" на странице и кликаем
        add_buttons = driver.find_elements(By.CSS_SELECTOR, ".add_to_cart_button")
        if add_buttons:
            add_buttons[0].click()
            print("✅ Товар (напиток/десерт) добавлен в корзину")
        else:
            print("⚠️ Не найдено товаров для добавления на странице меню")
        
        time.sleep(2)
        print("✅ Все товары добавлены в корзину")

    def get_total(self, driver):
        """Получает общую сумму заказа."""
        # Ждем появления элемента с итоговой суммой
        total_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".order-total .amount"))
        )
        text = total_element.text
        # Очищаем от символов валюты и пробелов
        # Пример: "1 234,56 ₽" -> 1234.56
        clean_text = text.replace('₽', '').replace(' ', '').replace(',', '.')
        total = float(clean_text)
        return total

    def apply_promo(self, driver, promo_code):
        """Применяет промокод на странице корзины."""
        # 1. Находим поле ввода промокода
        promo_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='coupon_code']"))
        )
        promo_input.clear()
        promo_input.send_keys(promo_code)
        print(f"Промокод '{promo_code}' введен")

        # 2. Нажимаем кнопку "Применить купон"
        apply_btn = driver.find_element(By.CSS_SELECTOR, "button[name='apply_coupon']")
        apply_btn.click()
        print("Кнопка 'Применить купон' нажата")

        # 3. Ждем обновления страницы: появления сообщения об успехе или ошибке
        time.sleep(3)  # Небольшая пауза для AJAX-запроса

        # 4. Проверяем, появилось ли сообщение об успешном применении
        try:
            success_msg = driver.find_element(By.CSS_SELECTOR, ".woocommerce-message")
            print(f"Сообщение от сайта: {success_msg.text}")
            return True
        except:
            # Если сообщения об успехе нет, проверяем, нет ли ошибки
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error")
                print(f"Ошибка при применении промокода: {error_msg.text}")
                return False
            except:
                print("Не удалось определить результат применения промокода")
                return False

    def fill_checkout_form(self, driver):
        """Заполняет форму оформления заказа."""
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "billing_first_name"))
        )
        driver.find_element(By.ID, "billing_first_name").send_keys("Тест")
        driver.find_element(By.ID, "billing_last_name").send_keys("Тестов")
        driver.find_element(By.ID, "billing_phone").send_keys("+79991234567")
        select = Select(driver.find_element(By.ID, "billing_country"))
        select.select_by_value("RU")
        time.sleep(1)
        driver.find_element(By.ID, "billing_city").send_keys("Москва")
        driver.find_element(By.ID, "billing_address_1").send_keys("ул. Тестовая, д. 1")
        driver.find_element(By.ID, "billing_postcode").send_keys("123456")

    def complete_order(self, driver):
        """Оформляет заказ."""
        # 1. Нажимаем кнопку "Оформить заказ" на странице корзины
        checkout_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".checkout-button"))
        )
        checkout_btn.click()
        print("Переход к оформлению заказа")
        time.sleep(3)

        # 2. Заполняем форму
        self.fill_checkout_form(driver)
        print("Форма заполнена")

        # 3. Принимаем условия (если есть)
        try:
            terms = driver.find_element(By.ID, "terms")
            if not terms.is_selected():
                driver.execute_script("arguments[0].click();", terms)
                print("Условия приняты")
        except:
            print("Чекбокс условий не найден или уже принят")

        # 4. Нажимаем кнопку "Подтвердить заказ"
        place_order = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "place_order"))
        )
        driver.execute_script("arguments[0].click();", place_order)
        print("Кнопка 'Подтвердить заказ' нажата")

        # 5. Ждем подтверждения заказа (появление сообщения об успехе или изменение URL)
        WebDriverWait(driver, 20).until(
            EC.any_of(
                EC.url_contains("order-received"),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".woocommerce-order-received"))
            )
        )
        print("✅ Заказ успешно оформлен!")

    # --- ОСНОВНОЙ ТЕСТ-КЕЙС ---
    @allure.story("Сценарий №4: Повторное применение промокода")
    @allure.title("Проверка, что промокод GIVEMEHALYAVA не применяется повторно (поиск бага)")
    def test_promo_code_twice(self, driver):
        main_page = MainPage(driver)
        auth_page = AuthPage(driver)

        with allure.step("1. Авторизация"):
            main_page.open_main_page()
            auth_page.open_my_account()
            auth_page.login(self.TEST_USERNAME, self.TEST_PASSWORD)
            time.sleep(3)
            print("✅ Авторизация выполнена")

        with allure.step("2. Очистка корзины перед тестом"):
            self.clear_cart(driver)

        # ========== ПЕРВЫЙ ЗАКАЗ ==========
        with allure.step("3. Добавить товары в корзину (2 пиццы + 1 напиток)"):
            self.add_items_to_cart(driver, main_page)

        with allure.step("4. Перейти на страницу корзины"):
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(3)

        with allure.step("5. Применить промокод GIVEMEHALYAVA (ПЕРВЫЙ РАЗ)"):
            total_before = self.get_total(driver)
            print(f"Сумма ДО применения: {total_before}")
            
            applied = self.apply_promo(driver, "GIVEMEHALYAVA")
            assert applied, "Промокод не применился в первый раз! Тест не может продолжаться."
            
            total_after = self.get_total(driver)
            print(f"Сумма ПОСЛЕ применения: {total_after}")
            assert total_after < total_before, "Сумма не уменьшилась. Скидка не применена."
            print("✅ Промокод успешно применился (первый заказ)")

        with allure.step("6. Оформить первый заказ"):
            self.complete_order(driver)

        # ========== ВТОРОЙ ЗАКАЗ ==========
        with allure.step("7. Перейти на главную страницу для нового заказа"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(3)

        with allure.step("8. Снова добавить товары в корзину"):
            self.add_items_to_cart(driver, main_page)

        with allure.step("9. Перейти на страницу корзины"):
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(3)

        with allure.step("10. Применить промокод GIVEMEHALYAVA (ВТОРОЙ РАЗ)"):
            total2_before = self.get_total(driver)
            print(f"Сумма ДО второго применения: {total2_before}")
            
            applied_again = self.apply_promo(driver, "GIVEMEHALYAVA")
            
            total2_after = self.get_total(driver)
            print(f"Сумма ПОСЛЕ второго применения: {total2_after}")

        # ========== ПРОВЕРКА И СОЗДАНИЕ БАГ-РЕПОРТА ==========
        with allure.step("11. ПРОВЕРКА: Промокод не должен применяться повторно"):
            print("\n" + "="*60)
            print("РЕЗУЛЬТАТ ПРОВЕРКИ СЦЕНАРИЯ №4:")
            print(f"Первый заказ: {total_before} → {total_after} (скидка {total_before - total_after} ₽)")
            print(f"Второй заказ: {total2_before} → {total2_after}")

            if applied_again and total2_after < total2_before:
                # БАГ НАЙДЕН! Промокод применился повторно.
                print("\n❌❌❌ БАГ ОБНАРУЖЕН! ❌❌❌")
                print("Промокод 'GIVEMEHALYAVA' применился повторно, хотя должен был сработать только один раз.")
                
                # Формируем текст баг-репорта
                bug_report_text = f"""
                БАГ-РЕПОРТ
                ===========
                Заголовок: Промокод GIVEMEHALYAVA применяется повторно для одного пользователя.
                Приоритет: Высокий (High)
                
                Окружение: Сайт https://pizzeria.skillbox.cc, браузер Chrome
                
                Шаги воспроизведения:
                1. Авторизоваться пользователем {self.TEST_USERNAME}
                2. Добавить любые товары в корзину
                3. На странице корзины применить промокод GIVEMEHALYAVA
                4. Оформить заказ
                5. Снова добавить любые товары в корзину
                6. На странице корзины снова применить промокод GIVEMEHALYAVA
                
                Ожидаемый результат:
                Промокод не применяется, сумма заказа не меняется. Система сообщает, что промокод уже был использован.
                
                Фактический результат:
                Промокод применился повторно, сумма заказа уменьшилась на 10%.
                Сумма до применения: {total2_before} ₽
                Сумма после применения: {total2_after} ₽
                
                Приложение: Скриншот страницы корзины после повторного применения.
                """
                print(bug_report_text)
                
                # Прикрепляем баг-репорт к Allure-отчету
                allure.attach(bug_report_text, name="Баг-репорт", attachment_type=allure.attachment_type.TEXT)
                
                # Делаем скриншот для наглядности
                driver.save_screenshot("bug_promo_reuse.png")
                with open("bug_promo_reuse.png", "rb") as f:
                    allure.attach(f.read(), name="Скриншот корзины с повторной скидкой", attachment_type=allure.attachment_type.PNG)
                
                # Завершаем тест с ошибкой, так как баг найден
                assert False, "БАГ: Промокод применяется повторно!"
            else:
                print("\n✅ Промокод НЕ применился повторно. Тест пройден (баг не воспроизвелся).")
                # Если баг не воспроизвелся, но мы ожидаем его по заданию, это тоже может быть интересно.
                allure.attach("Повторное применение промокода не сработало. Баг не обнаружен.", 
                              name="Результат проверки", 
                              attachment_type=allure.attachment_type.TEXT)

        with allure.step("12. (Опционально) Оформить второй заказ"):
            # Этот шаг необязателен для проверки бага, но добавим для чистоты эксперимента
            try:
                self.complete_order(driver)
                print("Второй заказ также оформлен (хотя промокод мог и не примениться).")
            except Exception as e:
                print(f"Не удалось оформить второй заказ: {e}")