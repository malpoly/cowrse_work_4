from abc import ABC, abstractmethod
import json
import os


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

    def __init__(self, name, url, salary, description):
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description

    def __str__(self):
        return f"name: {self.name},\n" \
               f"url: {self.url},\n" \
               f"salary:{self.salary},\n" \
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
            'page': page,
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
                name = vacancy['name']
                if vacancy['salary'] is None:
                    salary = 0
                elif vacancy['salary']['from'] is None:
                    salary = vacancy['salary']['to']
                elif vacancy['salary']['to'] is None:
                    salary = vacancy['salary']['from']
                else:
                    salary = f"от {vacancy['salary']['from']} до {vacancy['salary']['to']}"
                description = vacancy['snippet']['requirement']
                url = vacancy['alternate_url']
                vacancy = Vacancy(name, url, salary, description)
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
                  'count': 100,
                  }
        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies_data = data['objects']
            vacancies = []
            for vacancy in vacancies_data:
                name = vacancy['profession']
                if vacancy['payment_to'] and vacancy['payment_from'] is None or vacancy['payment_to'] == 0 and vacancy['payment_from'] == 0:
                    salary = 0
                elif vacancy['payment_from'] is None or vacancy['payment_from'] == 0:
                    salary = vacancy['payment_to']
                elif vacancy['payment_to'] is None or vacancy['payment_to'] == 0:
                    salary = vacancy['payment_from']
                else:
                    salary = f"от {vacancy['payment_from']} до {vacancy['payment_to']}"
                description = vacancy['candidat']
                url = vacancy['link']
                vacancy = Vacancy(name, url, salary, description)
                vacancies.append(vacancy)
            return vacancies
        else:
            return f'Error: {response.status_code}'



class Save(ABC):
    """Абстрактный класс, для добавления вакансий в файл json,
    получения данных из файла json по указанным критериям"""

    @abstractmethod
    def save_hh(self, headhunter):
        """
        Cохраняет данные о вакансиях в файл JSON
        :param headhunter - список с вакансиями с HH
        """
        pass


class JSONSaver(Save):
    """Класс для сбора данных о вакансиях с двух сайтов, их анализу и сохранению в файл"""
    def __init__(self):
        """Инициализатор класс"""
        self.file_name: str = 'Vacancy.json'

    def save_hh(self, headhunter):
        """
        Cохраняет данные о вакансиях в файл JSON
        :param headhunter - список с вакансиями с HH
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(headhunter, file, ensure_ascii=False, indent=4)


test_sj = SJAPI()
my_test = test_sj.get_vacancy("python")
for i in my_test:
    print(i)

test_hh = HHAPI()
my_test = test_hh.get_vacancy("python")
for i in my_test:
    print(i)
























