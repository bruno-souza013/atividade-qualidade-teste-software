from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


def reset_server():
    resp = requests.get("http://localhost:5000/users")
    if resp.status_code == 200:
        for u in resp.json():
            requests.delete(f"http://localhost:5000/users/{u['id']}")


def test_create_two_users_e2e():
    reset_server()

    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:5000")

        assert driver.title == "Users"

        wait = WebDriverWait(driver, 5)

        name_input = wait.until(EC.presence_of_element_located((By.ID, "name")))

        #primeiro usuario
        name_input.clear()
        name_input.send_keys("Usuario1")
        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: any("Usuario1" in li.text for li in d.find_elements(By.TAG_NAME, "li")))

        assert any("Usuario1" in li.text for li in driver.find_elements(By.TAG_NAME, "li"))

        #segundo usuario
        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys("Usuario2")
        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: any("Usuario2" in li.text for li in d.find_elements(By.TAG_NAME, "li")))

        #busca todos e valida os dois
        items = driver.find_elements(By.TAG_NAME, "li")
        texts = [i.text for i in items]
        assert "Usuario1" in texts and "Usuario2" in texts

    finally:
        driver.quit()


def test_initially_no_users_then_create_one_ui():
    reset_server()

    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:5000")

        wait = WebDriverWait(driver, 5)

        wait.until(EC.presence_of_element_located((By.ID, "name")))

        items = driver.find_elements(By.TAG_NAME, "li")
        assert len(items) == 0

        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys("João")
        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: any("João" in li.text for li in d.find_elements(By.TAG_NAME, "li")))

        items = driver.find_elements(By.TAG_NAME, "li")
        texts = [i.text for i in items]
        assert "João" in texts

    finally:
        driver.quit()


def test_api_created_user_shown_then_add_second_via_ui():
    reset_server()

    resp = requests.post("http://localhost:5000/users", json={"name": "Maria"})
    assert resp.status_code == 201

    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:5000")

        wait = WebDriverWait(driver, 5)
        wait.until(lambda d: any("Maria" in li.text for li in d.find_elements(By.TAG_NAME, "li")))

        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys("Lucas")
        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: any("Lucas" in li.text for li in d.find_elements(By.TAG_NAME, "li")))

        items = driver.find_elements(By.TAG_NAME, "li")
        texts = [i.text for i in items]
        assert "Maria" in texts and "Lucas" in texts

    finally:
        driver.quit()
