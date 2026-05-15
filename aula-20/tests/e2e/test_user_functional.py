from selenium import webdriver
from selenium.webdriver.common.by import By
from requests import get, delete


def test_create_user_e2e():
    driver = webdriver.Chrome()

    driver.get("http://localhost:5000")

    input_name = driver.find_element(By.ID, "name")
    input_name.send_keys("Bruno")

    button = driver.find_element(By.ID, "submit")
    button.click()

    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, 5)

    wait.until(
        lambda d: any("Bruno" in el.text for el in d.find_elements(By.TAG_NAME, "li"))
    )
    users = driver.find_elements(By.TAG_NAME, "li")

    assert any("Bruno" in user.text for user in users)

    driver.quit()


def test_create_two_users_e2e():

    # Limpar api antes do novo teste
    resp = get("http://localhost:5000/users")
    for u in resp.json():
        delete(f"http://localhost:5000/users/{u['id']}")

    driver = webdriver.Chrome()

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

        wait.until(
            lambda d, n=name: any(
                n in li.text for li in d.find_elements(By.TAG_NAME, "li")
            )
        )

    users = driver.find_elements(By.TAG_NAME, "li")
    texts = [u.text for u in users]

    assert "Marcelo" in texts and "Leonardo" in texts

    driver.quit()
