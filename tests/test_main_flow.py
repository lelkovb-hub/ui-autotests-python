import allure
import time
from selenium.webdriver.common.by import By
from pages.main_page import MainPage


@allure.feature("Основной флоу")
class TestMainFlow:

    @allure.story("Главная страница")
    @allure.title("Проверка открытия главной страницы")
    def test_open_main_page(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        assert "pizzeria" in driver.title.lower(), "Страница не загрузилась"
        print("Тест 1 пройден")

    @allure.story("Слайдер с пиццами")
    @allure.title("Проверка добавления пиццы в корзину из слайдера")
    def test_add_pizza_to_cart_from_slider(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        pizzas = main_page.get_slider_pizzas()
        assert len(pizzas) > 0, "Слайдер пуст"
        result = main_page.add_pizza_to_cart_by_index(0)
        assert result, "Не удалось добавить пиццу"
        time.sleep(2)
        main_page.go_to_cart()
        assert "cart" in driver.current_url, "Не перешли в корзину"
        print("Тест 2 пройден")