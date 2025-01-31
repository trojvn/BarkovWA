import logging
from pathlib import Path
from time import sleep

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from envs import SLEEP_END, USER

URL = "https://vk.barkov.net/whatsappsearch.aspx"

KW_FILE = Path("kw.txt")
BL_FILE = Path("bl.txt")


def get_lines(file: Path) -> list[str]:
    with file.open("r", encoding="utf-8") as f:
        return list(filter(None, [line.strip() for line in f.readlines()]))


def set_lines(file: Path, lines: list[str]):
    with file.open("w", encoding="utf-8") as f:
        f.writelines(lines)


def get_keyword() -> str:
    if not KW_FILE.is_file():
        KW_FILE.touch()
    if not BL_FILE.is_file():
        BL_FILE.touch()
    if lines := get_lines(KW_FILE):
        _bl = get_lines(BL_FILE)
        for l in lines:
            if l in _bl:
                continue
            kw = l
            set_lines(BL_FILE, _bl)
            return kw
    return ""


def _get(driver: uc.Chrome) -> bool:
    driver.implicitly_wait(100)
    xpath = "//*[@value='Скачать результат' or text()=' Скачать результат']"
    element = driver.find_element(By.XPATH, xpath)
    print("finded1")
    driver.implicitly_wait(5)
    is_clicked = False
    for _ in range(10):
        sleep(5)
        xpath = "//*[@value='Скачать результат' or text()=' Скачать результат']"
        try:
            element = driver.find_element(By.XPATH, xpath)
            print("finded2")
            element.click()
            is_clicked = True
            break
        except Exception:
            pass
    print(f"sleep {SLEEP_END}")
    sleep(SLEEP_END)
    return is_clicked


def _main():
    if not (kw := get_keyword()):
        print("No keywords!")
        return False
    print(f"new keyword {kw}")
    options = Options()
    user_dir = rf"C:\Users\{USER}\AppData\Local\Google\Chrome\User Data"
    driver = uc.Chrome(options, user_data_dir=user_dir, use_subprocess=True)
    try:
        driver.implicitly_wait(30)
        driver.get(URL)
        sleep(3)
        xpath = "//input[@placeholder='например, SMM']"
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        element.send_keys(kw)
        xpath = "//*[contains(text(),'Только ссылки на чаты вида')]"
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        sleep(3)
        xpath = "//input[@id='submitWhatsappSearch']"
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        if _get(driver):
            _bl = get_lines(BL_FILE)
            _bl.append(f"\n{kw}")
            set_lines(BL_FILE, _bl)
    except Exception as e:
        logging.exception(e)
    driver.close()
    return True


def main():
    while True:
        try:
            if not _main():
                break
        except Exception:
            pass
    input("Enter for exit...")


if __name__ == "__main__":
    main()
