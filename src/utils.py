import json
from classes import Engine, Vacancy, HHAPI, SJAPI, Save, JSONSaver


def user_interaction():
    """
    Функция для получения от пользователя данных для запроса поиска вакансии на ресурсах
    :return: website - данные по платформе поиска вакансий, keyword -  кодовое слово для поиска
    """
    while True:
        website = input(
            f'На каком сайте будем искать? ("1" - HeadHunter | "2" - SuperJob | "0" - на всех | "stop" - выход'
            f' | при вводе другой информации программа завершится): ')
        if website == 'stop':
            return 'stop'
        elif website in ('0', '1', '2'):
            break
        else:
            return 'stop'

    keyword = input('Введите поисковый запрос для поиска вакансии ("stop" - выход): ')
    if keyword == 'stop':
        return 'stop'
    return website, keyword

def get_information(website, keyword):
    """
    Функция для получения информации с вебсайтов
    :return:
    """
    if website == '1':
        hh = HHAPI()
        return hh.get_vacancy(keyword), None
    elif website == '2':
        sj = SJAPI()
        return None, sj.get_vacancy(keyword)
    else:
        hh = HHAPI()
        sj = SJAPI()
        return hh.get_vacancy(keyword), sj.get_vacancy(keyword)


def write_json(hh_vacancy, sj_vacancy):
    """
    Функция записывает данные по вакансиям в файл json
    :return: записанный файл json
    """
    new_file = JSONSaver()
    return new_file.save_json(hh_vacancy, sj_vacancy)

def salary_filter():
    """
    Открывает записанный файл с вакансиями, перебирает вакансии, оставляет только те,
    которые подходят по зарплате, указанной пользователем
    :param salary_input: требуемая зарплата
    :return: новый список вакансий, с требуемой зарплатой
    """
    salary_input = input(f'Укажите требуемую зарплату, в рублях: ')

    with open("VacancyJson", 'r', encoding='utf-8') as file:
        all_vacancy = json.load(file)

    good_salary = [] #список для вакансий с подходящей зарплатой

    for vacancy in all_vacancy:
        if vacancy["salary_from"] >= int(salary_input):
            good_salary.append(vacancy)

    with open("VacancyJson", 'w', encoding='utf-8') as file:
        json.dump(good_salary, file, ensure_ascii=False, indent=4)


def description_filter():
    """ Поиск вакансий по заданным словам в созданном файле json. Возвращает новый файл"""
    words = input(f'Введите слово для поиска в описании: ')
    description_vacancy = []
    with open("VacancyJson", 'r', encoding='utf-8') as file:
        all_vacancy = json.load(file)
    for vac in all_vacancy:
        if isinstance(vac['description'], str):
            if words.lower() in vac['description'].lower():
                description_vacancy.append(vac)
    with open("VacancyJson", 'w', encoding='utf-8') as file:
        json.dump(description_vacancy, file, ensure_ascii=False, indent=4)


def top_vacancy():
    """
    Возвращает заданное колличество вакансий
    """
    print('Введите количество вакансий для просмотра:')
    n = input()
    new_vacancy = []
    with open("VacancyJson", 'r', encoding='utf-8') as file:
        all_vacancy = json.load(file)
    if int(n) >= len(all_vacancy):
        new_vacancy = all_vacancy
    else:
        for vacancy in all_vacancy:
            while int(n) > len(new_vacancy):
                new_vacancy.append(vacancy)
    with open("VacancyJson", 'w', encoding='utf-8') as file:
        json.dump(new_vacancy, file, ensure_ascii=False, indent=4)
