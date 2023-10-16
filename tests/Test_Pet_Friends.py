import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_All_pets_are_present(): # Присутствуют все питомцы
    # Неявное ожидание
    pytest.driver.implicitly_wait(10)

    # Подсчет карточек питомцев
    number_of_pets_1 = pytest.driver.find_elements(By.CSS_SELECTOR, '.table tbody tr')

    # Поиск количества карточек в статистике
    element = pytest.driver.find_element(By.XPATH, '//*[@class="task3 fill"]')
    import re
    pattern = r'Питомцев: (\d+)'
    match = re.search(pattern, element.text)
    if match:
        number_of_pets_2 = int(match.group(1))

    # Сравнение результатов
    assert len(number_of_pets_1) == number_of_pets_2


def test_At_least_half_of_the_pets_have_a_photo(): # Хотя бы у половины питомцев есть фото
    table = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-hover"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Подсчет количества строк с фото
    photos_count = 0

    # Проход по каждой строке, пропуская заголовок таблицы
    for row in rows[1:]:
        photo = row.find_element(By.TAG_NAME, "img").get_attribute("src")
        if photo:
            photos_count += 1

    # Проверка условия, что питомцев с фотографией половина или более
    assert photos_count >= (len(rows[1:]) / 2)


def test_All_pets_have_a_name_age_and_breed(): # У всех питомцев есть имя, возраст и порода
    table = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-hover"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Проверка для каждого питомца
    for row in rows[1:]:
        pet_info = row.find_elements(By.TAG_NAME, "td")
        assert pet_info[0].text, "У питомца отсутствует имя"
        assert pet_info[1].text, "У питомца отсутствует порода"
        assert pet_info[2].text, "У питомца отсутствует возраст"


def test_All_pets_have_different_names(): # У всех питомцев разные имена
    pytest.driver.implicitly_wait(10)

    # Находим все элементы с именами питомцев
    pet_names = pytest.driver.find_elements(By.XPATH, "//td[position() = 1]")

    # Проверяем уникальность имен
    names = []
    for pet_name in pet_names:
        name = pet_name.text.strip()
        if name in names:
            pytest.fail(f"Повторяющееся имя питомца: {name}")
        names.append(name)

def test_There_are_no_duplicate_pets_in_the_list(): # В списке нет повторяющихся питомцев
    pytest.driver.implicitly_wait(10)

    pet_table_rows = pytest.driver.find_elements(By.XPATH, "//tbody/tr")

    pets = []
    for row in pet_table_rows:
        # Извлекаем значение имени, породы и возраста из каждой строки таблицы
        pet_name = row.find_element(By.XPATH, "./td[1]").text.strip()
        pet_breed = row.find_element(By.XPATH, "./td[2]").text.strip()
        pet_age = row.find_element(By.XPATH, "./td[3]").text.strip()
        # Создаем кортеж с именем, породой и возрастом
        pet = (pet_name, pet_breed, pet_age)

        # Ищем одинаковых питомцев
        if pet in pets:
            pytest.fail(f"Найден дублирующийся питомец: {pet}")
        pets.append(pet)