from engine import Engine
from vacancy import Vacancy
import requests


class HHAPI(Engine):
    """Класс для получения данных по API с сайта HH"""

    def __init__(self):
        self.hh_url = "https://api.hh.ru/vacancies"

    def get_vacancy(self, keyword):
        """Метод, который получает данные по API с сайта HH и записывает данные в экземпляр класса Vacancy"""
        params = {'text': keyword,
                  'per_page': 100,
                  'area': 113
                  }
        response = requests.get(self.hh_url, params=params)

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
                #salary = vacancy['salary']
                description = vacancy['snippet']['requirement']
                url = vacancy['alternate_url']
                vacancy = Vacancy(name, url, salary, description)
                vacancies.append(vacancy)
            return vacancies
        else:
            return f'Error: {response.status_code}'

test_hh = HHAPI()
my_test= test_hh.get_vacancy("python")
for i in my_test:
    print(i)


