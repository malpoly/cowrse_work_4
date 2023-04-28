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
    salary_input = input(f'Укажите требуемую зарплату, в рублях,: ')

    with open("VacancyJson", 'r', encoding='utf-8') as file:
        all_vacancy = json.load(file)

    good_salary = [] #список для вакансий с подходящей зарплатой

    for vacancy in all_vacancy:
        if vacancy["salary_from"] >= int(salary_input):
            good_salary.append(vacancy)

    with open("VacancyJson", 'w', encoding='utf-8') as file:
        json.dump(good_salary, file, ensure_ascii=False, indent=4)

