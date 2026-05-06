import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# Запускаем браузер напрямую (без фикстур)
driver = webdriver.Chrome()
driver.maximize_window()

try:
    print("\n=== ОТЛАДКА: ПОИСК ССЫЛКИ 'МОЙ АККАУНТ' ===\n")
    
    # Открываем главную страницу
    driver.get("https://pizzeria.skillbox.cc/")
    time.sleep(3)
    
    # Ищем все ссылки
    all_links = driver.find_elements(By.TAG_NAME, "a")
    print("Все ссылки на главной странице:")
    for link in all_links:
        text = link.text.strip()
        href = link.get_attribute("href")
        if text:
            print(f"  [{text}] -> {href}")
    
    print("\n" + "="*50 + "\n")
    
    # Пробуем найти ссылку на аккаунт
    account_link = None
    
    # Способ 1: по тексту
    try:
        account_link = driver.find_element(By.XPATH, "//a[contains(text(),'Аккаунт') or contains(text(),'аккаунт')]")
        print(f"Найдено по тексту: {account_link.text}")
    except:
        print("Способ 1: не найдено")
    
    # Способ 2: по href
    try:
        account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'my-account') or contains(@href, 'account')]")
        print(f"Найдено по href: {account_link.text} -> {account_link.get_attribute('href')}")
    except:
        print("Способ 2: не найдено")
    
    # Способ 3: ищем в меню
    try:
        menu_items = driver.find_elements(By.CSS_SELECTOR, ".menu-item, .nav-menu li, header li")
        for item in menu_items:
            if "аккаунт" in item.text.lower() or "account" in item.text.lower():
                print(f"Найдено в меню: {item.text}")
                account_link = item.find_element(By.TAG_NAME, "a")
                break
    except:
        print("Способ 3: не найдено")
    
    if account_link:
        print(f"\n✅ Найдена ссылка: {account_link.text}")
        account_link.click()
        time.sleep(3)
        print(f"Текущий URL: {driver.current_url}")
        
        # Проверяем, есть ли форма регистрации
        page_text = driver.page_source.lower()
        if "register" in page_text or "регистрац" in page_text:
            print("✅ На странице есть форма регистрации")
        else:
            print("⚠️ Форма регистрации не обнаружена")
            
        # Выводим все поля ввода
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print("\nПоля ввода на странице:")
        for inp in inputs:
            inp_id = inp.get_attribute("id")
            inp_name = inp.get_attribute("name")
            inp_type = inp.get_attribute("type")
            if inp_id or inp_name:
                print(f"  - id={inp_id}, name={inp_name}, type={inp_type}")
    
except Exception as e:
    print(f"Ошибка: {e}")

finally:
    print("\n=== ОТЛАДКА ЗАВЕРШЕНА ===")
    input("Нажми Enter для закрытия браузера...")
    driver.quit()