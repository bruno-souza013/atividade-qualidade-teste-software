from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from requests import get, delete


def text_in_list(driver, text):
    """Verifica se 'text' aparece em algum <li>, ignorando StaleElementReferenceException."""
    try:
        items = driver.find_elements(By.TAG_NAME, "li")
        return any(text in li.text for li in items)
    except StaleElementReferenceException:
        return False


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def test_create_user_e2e():
    driver = get_driver()

    driver.get("http://localhost:5000")

    input_name = driver.find_element(By.ID, "name")
    input_name.send_keys("Bruno")

    button = driver.find_element(By.ID, "submit")
    button.click()

    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, 10)

    wait.until(lambda d: text_in_list(d, "Bruno"))

    assert text_in_list(driver, "Bruno")

    driver.quit()


def test_create_two_users_e2e():

    # Limpar api antes do novo teste
    resp = get("http://localhost:5000/users")
    for u in resp.json():
        delete(f"http://localhost:5000/users/{u['id']}")

    driver = get_driver()

    driver.get("http://localhost:5000")

    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, 5)

    names = ["Marcelo", "Leonardo"]

    for name in names:
        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys(name)

        submit = driver.find_element(By.ID, "submit")
        submit.click()

        wait.until(lambda d, n=name: text_in_list(d, n))

    users = driver.find_elements(By.TAG_NAME, "li")
    texts = [u.text for u in users]

    assert "Marcelo" in texts and "Leonardo" in texts

    driver.quit()
