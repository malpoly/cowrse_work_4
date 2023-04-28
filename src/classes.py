import json
import requests
from abc import ABC, abstractmethod


EXCHANGE_RATE = 90  # курс перевода зарплаты в рубли

class Engine(ABC):
    """Абстрактный класс для сбора данных с сайтов вакансии"""

    @abstractmethod
    def get_vacancy(self, keyword):
        """метод для прлучения данных
        :param keyword - исходный запрос от пользователя
        возвращает список объектов класса Vacancy"""
        pass


class Vacancy():
    """
    Класс для работы с вакансиями
    :param name - название вакансии,
    :param url - ссылка на вакансию,
    :param salary - зарплата,
    :param description - краткое описание
    """

    def __init__(self, website, name, url, salary_from, salary_to, description)-> None:
        self.website: str = website
        self.name: str = name
        self.url: str = url
        self.salary_from: int = salary_from
        self.salary_to: int = salary_to
        self.description = description

    def __str__(self):
        return f"website: {self.website},\n" \
               f"name: {self.name},\n" \
               f"url: {self.url},\n" \
               f"salary:{self.salary_from if self.salary_from else 0} -> " \
               f"{self.salary_to if self.salary_to else ''} руб/мес\n" \
               f"description: {self.description}"


class HHAPI(Engine):
    """Класс для получения данных по API с сайта HH"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def get_vacancy(self, keyword):
        """Метод, который получает данные по API с сайта HH и записывает данные в экземпляр класса Vacancy"""
        params = {
            'text': keyword,
            'area': 113,
            'per_page': 100,
            'only_with_salary': True,
            'search_field': 'name'
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies_data = data['items']
            vacancies = []
            for vacancy in vacancies_data:
                website = "headhunter"
                name = vacancy['name']
                if vacancy['salary']['from'] is None:
                    salary_from = 0
                else:
                    if vacancy['salary']['currency'] == 'RUR':
                        salary_from = vacancy['salary']['from']
                    else:
                        salary_from = vacancy['salary']['from'] * EXCHANGE_RATE
                if vacancy['salary']['to'] is None:
                    salary_to = 0
                else:
                    if vacancy['salary']['currency'] == 'RUR':
                        salary_to = vacancy['salary']['to']
                    else:
                        salary_to = vacancy['salary']['to'] * EXCHANGE_RATE
                description = vacancy['snippet']['requirement']
                url = vacancy['alternate_url']
                vacancy = Vacancy(website, name, url, salary_from, salary_to, description)
                vacancies.append(vacancy)
            return vacancies
        else:
            return f'Error: {response.status_code}'


class SJAPI(Engine):
    """Класс для получения данных по API с сайта SJ"""

    def __init__(self):
        """ Инициализатор класса."""
        self.id = "v3.r.137504425.3bd774d8e085a6556a964c482ee28bd1837a8af5.228d65db66f8f2ff2389edf45434bf78242f3d4d"
        self.headers = {'X-Api-App-Id': self.id}
        self.url = "https://api.superjob.ru/2.0/vacancies/"

    def get_vacancy(self, keyword):
        """Метод, который получает данные по API с сайта HH и записывает данные в экземпляр класса Vacancy"""
        params = {'keyword': keyword,
                  'c': 1,
                  'count': 100,
                  'only_with_salary': True,
                  }
        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies_data = data['objects']
            vacancies = []
            for vacancy in vacancies_data:
                website = "superjob"
                name = vacancy['profession']
                if vacancy['payment_from'] is None:
                    salary_from = 0
                else:
                    if vacancy['currency'] == 'rub':
                        salary_from = vacancy['payment_from']
                    else:
                        salary_from = vacancy['payment_from'] * EXCHANGE_RATE
                if vacancy['payment_to'] is None:
                    salary_to = 0
                else:
                    if vacancy['currency'] == 'rub':
                        salary_to = vacancy['payment_to']
                    else:
                        salary_to = vacancy['payment_to'] * EXCHANGE_RATE
                description = vacancy['candidat']
                url = vacancy['link']
                vacancy = Vacancy(website, name, url, salary_from, salary_to, description)
                vacancies.append(vacancy)
            return vacancies
        else:
            return f'Error: {response.status_code}'


class Save(ABC):
    """Абстрактный класс, для добавления вакансий в файл json,
    получения данных из файла json по указанным критериям"""

    @abstractmethod
    def save_json(self, data_hh: list[dict], data_sj: list[dict]) -> None:
        pass


class JSONSaver(Save):
    """Класс для сбора данных о вакансиях с двух сайтов, их анализу и сохранению в файл"""
    def __init__(self) -> None:
        """Инициализатор класс"""
        self.filename = "VacancyJson"  # при инициализации экземпляра

    def save_json(self, data_hh: list[dict]=None, data_sj: list[dict]=None) -> None:
        """
        Cохраняет данные о вакансиях в файл JSON
        :param data_hh - список с вакансиями с HH, по умолчанию None
        :param data_sj - список с вакансиями с SJ, по умолчанию None
        """
        if data_hh is not None and data_sj is None:
            # вариант, когда нет данных по сайту SJ
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(sorted([vars(vacancy) for vacancy in data_hh], key=lambda x: x['salary_from'],
                                 reverse=True), file, ensure_ascii=False, indent=4)
        elif data_hh is None and data_sj is not None:
            # вариант, когда нет данных по сайту HH
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(sorted([vars(vacancy) for vacancy in data_sj], key=lambda x: x['salary_from'],
                                 reverse=True), file, ensure_ascii=False, indent=4)
        elif data_hh is None and data_sj is None:
            print('Нет данных по вакансиям')
        else:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(sorted([vars(vacancy) for vacancy in data_hh + data_sj], key=lambda x: x['salary_from'],
                                 reverse=True),file, ensure_ascii=False, indent=4)

























