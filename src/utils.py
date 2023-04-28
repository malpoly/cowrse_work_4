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
    :return:
    """
    new_file = JSONSaver()
    return new_file.save_json(hh_vacancy, sj_vacancy)