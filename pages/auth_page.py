import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AuthPage(BasePage):
    # Локаторы для страницы входа (my-account)
    LOGIN_USERNAME = (By.ID, "username")
    LOGIN_PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.NAME, "login")
    
    # Ссылка на страницу аккаунта
    MY_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href*='my-account']")

    def open_my_account(self):
        """Открывает страницу 'Мой аккаунт'."""
        self.click(self.MY_ACCOUNT_LINK)
        time.sleep(2)

    def login(self, username, password):
        """Выполняет вход существующего пользователя."""
        # Вводим логин/email
        username_input = self.wait.until(
            EC.presence_of_element_located(self.LOGIN_USERNAME)
        )
        username_input.clear()
        username_input.send_keys(username)
        
        # Вводим пароль
        password_input = self.driver.find_element(*self.LOGIN_PASSWORD)
        password_input.clear()
        password_input.send_keys(password)
        
        # Нажимаем кнопку входа
        self.click(self.LOGIN_BTN)
        time.sleep(3)

    def is_logged_in(self):
        """Проверяет, что пользователь залогинен."""
        try:
            # Проверяем, что есть кнопка выхода или страница аккаунта
            logout_btn = self.driver.find_element(By.CSS_SELECTOR, "a[href*='logout'], .woocommerce-MyAccount-content")
            return logout_btn.is_displayed()
        except:
            return False