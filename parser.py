import requests
import sqlite3
from database import fill_vacancy


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def get_vacancies(city, vacancy, page):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f"{vacancy} {city}",
        'area': city,
        'specialization': 1,
        'per_page': 100,
        'page': page
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_vacancy_skills(vacancy_id):
    url = f'https://api.hh.ru/vacancies/{vacancy_id}'

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    skills = [skill['name'] for skill in data.get('key_skills', [])]
    return ', '.join(skills)


def get_industry(company_id):
    # Получение отрасли компании по ее идентификатору
    if company_id is None:
        return 'Unknown'

    url = f'https://api.hh.ru/employers/{company_id}'
    response = requests.get(url)
    if response.status_code == 404:
        return 'Unknown'
    response.raise_for_status()
    data = response.json()

    if 'industries' in data and len(data['industries']) > 0:
        return data['industries'][0].get('name')
    return 'Unknown'


def parse_vacancies():
    cities = {
        'Москва': 1,
        'Санкт-Петербург': 2
    }

    vacancies = [
        'Python Developer',
    ]

    for city, city_id in cities.items():
        for vacancy in vacancies:
            page = 0
            while True:
                try:
                    data = get_vacancies(city_id, vacancy, page)


                    if not data.get('items'):
                        break

                    for item in data['items']:
                        if vacancy.lower() not in item['name'].lower():
                            continue  # Пропустить, если название вакансии не совпадает

                        title = f"{item['name']} ({city})"
                        keywords = item['snippet'].get('requirement', '')
                        skills = get_vacancy_skills(item['id'])
                        company = item['employer']['name']
                        industry = get_industry(item['employer'].get('id'))
                        experience = item['experience'].get('name', '')
                        salary = item['salary']
                        if salary is None:
                            salary = "з/п не указана"
                        else:
                            salary = salary.get('from', '')
                        url = item['alternate_url']
                        
                        con = sqlite3.connect("tg.db")
                        cur = con.cursor()                        
                        fill_vacancy(cur, con, item['name'], company, salary, city, url)

                        if page >= data['pages'] - 1:
                            break

                        page += 1

                except requests.HTTPError as e:
                    continue  # Перейти к следующему городу, если произошла ошибка


parse_vacancies()
    