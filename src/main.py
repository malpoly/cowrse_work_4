from utils import user_interaction, get_information, write_json, salary_filter, description_filter, top_vacancy

#Главный файл для взаимодействия с пользователем:

website, keyword = user_interaction() #взаимодействие с подьзователем
hh_vacancy, sj_vacancy = get_information(website, keyword) #поиск по api
write_json(hh_vacancy, sj_vacancy) #запись в файл
salary_filter() #предлагаем пользователю ввести требуемую зарплату
description_filter() #предлагаем пользователю ввести слово в описании
top_vacancy() #предлагаем пользователю ввести количество вакансий для просмотра





