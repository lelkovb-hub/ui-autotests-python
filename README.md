# 🍕 UI автотесты для сайта Pizzeria

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.x-orange)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-Report-purple)](https://docs.qameta.io/allure/)

## 📋 О проекте

Финальная работа по курсу **«Автотесты на Python. Базовая часть»** (Skillbox).  
Набор **UI-автотестов** для сайта-пиццерии (учебный стенд).

- Язык: **Python 3.10**
- Фреймворк: **Pytest** + **Selenium WebDriver**
- Паттерн: **Page Object Model (POM)**
- Отчёты: **Allure** (настроен и используется)
- Линтер: **Flake8**

---

## 🎯 Что покрыто автотестами

| Модуль | Что проверяется |
|--------|------------------|
| **Авторизация** | Вход с валидными/невалидными данными, выход из аккаунта |
| **Корзина** | Добавление/удаление товаров, обновление количества, пересчёт суммы |
| **Промокоды** | Применение валидных/невалидных/просроченных промокодов |
| **Оформление заказа** | Заполнение формы, валидация полей, отправка заказа |

---

## 🐛 Найденные баги

В процессе написания и прогона автотестов выявлены дефекты.  
Подробный отчёт с описанием шагов воспроизведения и скриншотами:

👉 [**BUG_REPORT.md**](./BUG_REPORT.md)

**Примеры:**
- Повторное применение промокода к одному заказу
- Сообщения об ошибках на английском языке (требуется русский)
- Некорректная валидация поля «Телефон»

---

## 🚀 Как запустить проект

### 1️⃣ Клонировать репозиторий

git clone https://github.com/lelkovb-hub/ui-autotests-python.git
cd ui-autotests-python

### 2️⃣ Установить зависимости

pip install -r requirements.txt

### 3️⃣ Запустить все тесты

pytest -v

### 4️⃣ Сгенерировать и открыть Allure‑отчёт

pytest --alluredir=allure-results     
allure serve allure-results

После выполнения `allure serve` отчёт автоматически откроется в браузере по умолчанию.

---

## 📁 Структура проекта
```
ui-autotests-python/
├── pages/                  # Page Object classes
├── tests/                  # Test files
├── reports/                # HTML reports (if any)
├── logs/                   # Log files
├── conftest.py             # Pytest fixtures (driver, setup/teardown)
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
├── BUG_REPORT.md           # Bug report
└── bug_promo_reuse.png     # Screenshot for a specific bug
```

---

## 🛠 Использованные технологии

| Технология | Назначение |
|------------|------------|
| Python 3.10 | Язык программирования |
| Selenium WebDriver | Управление браузером |
| Pytest | Тестовый фреймворк |
| Allure | Визуальные отчёты (настроен, отчёты работают) |
| Page Object Model | Паттерн организации кода |
| Flake8 | Линтер (проверка стиля кода) |
| webdriver-manager | Автоматическое управление драйверами |
| Git | Контроль версий |

---

## 📈 Отчёты

Allure генерирует детальные визуальные отчёты с графиками, шагами тестов, скриншотами и логами.  
Команда `allure serve allure-results` открывает отчёт в браузере.

---

## 📝 Что можно улучшить

- HTML‑отчёты (pytest‑html)
- Настройка Allure (работает)
- Параллельный запуск тестов (pytest‑xdist)
- Интеграция с CI/CD (GitHub Actions)
- API‑тесты для бэкенда

---

## 📬 Контакты

**Борис Лельков**  
- Telegram: [@Boris80lb](https://t.me/Boris80lb)  
- Email: [lelkovb@gmail.com](mailto:lelkovb@gmail.com)  
- GitHub: [lelkovb-hub](https://github.com/lelkovb-hub)

---

*Проект выполнен в рамках обучения в Skillbox.*
