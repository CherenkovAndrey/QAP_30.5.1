import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import driver_path, valid_email, valid_password


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(driver_path)

   # Открытие страницы авторизации
   pytest.driver.set_window_size(1200, 800)
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   # Ввод email
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'email')))
   pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

   # Ввод пароля
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'pass')))
   pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

   # Вход в аккаунт
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Переход в "Мои питомцы"
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]')))
   pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()

   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'
   yield
   pytest.driver.quit()