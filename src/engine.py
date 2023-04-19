from abc import ABC, abstractmethod

class Engine(ABC):
    """Абстрактный класс для сбора данных с сайтов вакансии"""

    @abstractmethod
    def get_vacancy(self):
        pass