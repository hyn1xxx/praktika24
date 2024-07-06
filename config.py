TOKEN = '7102317527:AAEJsJ3n6rqqS0r3hwsTLXjDBVbRwoFMKyM'

start_msg = '''
Привет! Я помогу вам в поиске вакансий на платформе hh.ru.
Автор бота - Пшеничный Никита БВТ2205.
'''

def vacancy_msg(vacancy_name, company, salary, city, url):
    msg = f'Вакансия: {vacancy_name}\nКомпания: {company}\nЗарплата: {salary}\nГород: {city}\nСсылка: {url}'
    return msg
    
help = '''
Запустить бота /start
Посмотреть вакансии /vacancy
Список комманд /help
'''