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
               f"description: {self.description}" \
