import pytest
import logging
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s][%(asctime)s][%(name)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/test.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@pytest.fixture
def driver():
    logger.info("Запуск браузера")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    service = Service(r"C:\chromedriver-win64\chromedriver.exe")
    
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    logger.info("Закрытие браузера")
    driver.quit()