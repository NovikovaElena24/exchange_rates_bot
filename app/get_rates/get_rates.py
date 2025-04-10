# Other imports
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging


# Функция для выполнения GET-запроса с подменой User-Agent
def make_request(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Устанавливаем кодировку ответа сервера в UTF-8, чтобы корректно отображать кириллицу
            response.encoding = "utf-8"
            return response.text
        else:
            return f"Ошибка: получен статус-код {response.status_code}"
    except Exception as e:
        return f"Ошибка: {e}"


def get_mig_current_rate():

    # Создание словарей (покупка и продажа) с парами: валюта - значение
    mig_buy = dict()
    mig_sell = dict()

    # Задаем URL-адрес веб-страницы
    # url = "https://mig.kz/api/v1/gadget/html"
    url = "https://mig.kz"
    ua = UserAgent()

    # Генерация случайного User-Agent
    fake_ua = {"User-Agent": ua.random}

    # Отправляем GET-запрос к указанной странице
    response_text = make_request(url, fake_ua)

    if not response_text.startswith("Ошибка"):
        # Преобразуем текст ответа сервера в объект BeautifulSoup с использованием парсера 'lxml'
        soup = BeautifulSoup(response_text, "lxml")

        # Поиск тегов td c классом buy - поиск значений покупки валюты
        buy_rate = soup.select("table td.buy")
        # Поиск тегов td c классом currency - поиск названий валют
        currency = soup.select("table td.currency")
        # Поиск тегов td c классом buy - поиск значений покупки валюты
        sell_rate = soup.select("table td.sell")

        if len(buy_rate) == len(currency) == len(sell_rate):
            for i in range(len(buy_rate)):
                cur = currency[i].get_text().upper()
                if cur in ("USD", "RUB"):
                    mig_buy[cur] = float(buy_rate[i].get_text())
                    mig_sell[cur] = float(sell_rate[i].get_text())

    logging.debug(f"Курсы валют МиГ:")
    logging.debug(f"Покупка: {mig_buy}")
    logging.debug(f"Продажа: {mig_buy}")
    return mig_buy, mig_sell


def get_mig_official_rate():

    # Создание словаря с парами: валюта - значение
    official_rates = dict()

    # Задаем URL-адрес веб-страницы
    url = "https://mig.kz"
    ua = UserAgent()

    # Генерация случайного User-Agent
    fake_ua = {"User-Agent": ua.random}

    # Отправляем GET-запрос к указанной странице
    response_text = make_request(url, fake_ua)

    if not response_text.startswith("Ошибка"):
        # Преобразуем текст ответа сервера в объект BeautifulSoup с использованием парсера 'lxml'
        soup = BeautifulSoup(response_text, "lxml")

        # # Получение таблицы с официальным курсом
        # official_table = soup.find("div", class_="external-rates-wrapper").find("ul", class_="clearfix")
        # # Получение названий валюты
        # official_currency_table = official_table.find_all("h4")
        # # Получение значений курсов
        # official_rates_table = official_table.find_all("p")

        # Получение таблицы с официальным курсом
        official_table = soup.select_one("ul.clearfix")
        # Получение названий валюты
        official_currency_table = official_table.select("h4")
        # Получение значений курсов
        official_rates_table = official_table.select("p")

        for i in range(len(official_currency_table)):
            cur = official_currency_table[i].get_text().upper()
            if cur in ("USD", "RUB"):
                official_rates[cur] = float(
                    official_rates_table[i].get_text().split(" ")[0].strip()
                )

    logging.debug(f"Официальный курс НБ РК: {official_rates}")
    return official_rates


def get_cbr_official_rate():

    # Создание словаря с парами: валюта - значение
    official_rates = dict()

    # Задаем URL-адрес веб-страницы
    url = "https://www.cbr.ru/currency_base/daily/"
    ua = UserAgent()

    # Генерация случайного User-Agent
    fake_ua = {"User-Agent": ua.random}

    # Отправляем GET-запрос к указанной странице
    response_text = make_request(url, fake_ua)

    if not response_text.startswith("Ошибка"):
        # Преобразуем текст ответа сервера в объект BeautifulSoup с использованием парсера 'lxml'
        soup = BeautifulSoup(response_text, "lxml")

        # Получение таблицы с официальным курсом
        # official_table_rows = soup.find("table", class_="data").find_all("tr")
        official_table_rows = soup.select("table.data tr")

        # Поиск интересующих курсов валют
        for row in official_table_rows[1:]:  # Пропускаем заголовок таблицы
            columns = [d.get_text().strip() for d in row.select("td")]
            if len(columns) > 2 and columns[1].upper() in ("USD", "EUR", "KZT", "CNY"):
                official_rates[columns[1]] = round(
                    float(columns[-1].replace(",", ".")) / float(columns[2]), 2
                )

    logging.debug(f"Официальный курс ЦБ РФ: {official_rates}")
    return official_rates
