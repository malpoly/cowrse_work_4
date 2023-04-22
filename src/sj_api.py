from engine import Engine
from vacancy import Vacancy
import os
import requests

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

test_sj = SJAPI()
my_test = test_sj.get_vacancy("python")

for i in my_test:
    print(i)

