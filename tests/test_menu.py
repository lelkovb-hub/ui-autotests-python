import allure
import time
from selenium.webdriver.common.by import By
from pages.menu_page import MenuPage


@allure.feature("Меню")
class TestMenu:

    @allure.story("Категории")
    @allure.title("Проверка фильтрации десертов")
    def test_desserts_filter(self, driver):
        menu_page = MenuPage(driver)

        with allure.step("Открыть страницу меню"):
            menu_page.open_menu_page()

        with allure.step("Выбрать категорию 'Десерты'"):
            menu_page.select_desserts_category()
            time.sleep(2)

        with allure.step("Проверить, что отображаются товары"):
            count = menu_page.get_products_count()
            assert count > 0, "Нет товаров в категории Десерты"
            print(f"Найдено товаров: {count}")

        with allure.step("Проверить, что среди товаров есть десерты"):
            # Находим все названия товаров
            titles = driver.find_elements(By.CSS_SELECTOR, ".product-title, .woocommerce-loop-product__title, .product h3, .product .product-title, h3")
            titles_text = [t.text.lower() for t in titles if t.text]
            
            print(f"Названия товаров: {titles_text}")
            
            # Ключевые слова десертов
            dessert_keywords = ["десерт", "торт", "пирож", "чизкейк", "мусс", "кекс", "печень", "эклер", "булочка", "шоколад", "морковный"]
            
            # Проверяем, что хотя бы один товар — десерт
            has_dessert = any(any(keyword in title for keyword in dessert_keywords) for title in titles_text)
            assert has_dessert, "Среди товаров нет ни одного десерта"
            
            print("Проверка пройдена: десерты найдены")