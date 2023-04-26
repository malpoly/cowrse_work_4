from classes import Engine, Vacancy, HHAPI, SJAPI, Save, JSONSaver


def user_interaction():
    """
    Функция для получения от пользователя данных для запроса поиска вакансии на ресурсах
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


#my_test = user_interaction()
