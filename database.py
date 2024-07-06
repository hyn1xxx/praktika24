import sqlite3


con = sqlite3.connect("tg.db")
cur = con.cursor()


def table(cur, con):
    cur.execute("CREATE TABLE IF NOT EXISTS user ( tg_id int );")
    cur.execute("CREATE TABLE IF NOT EXISTS vacancy ( vacancy_name varchar(30), company varchar(30), salary varchar(30), city varchar (20), url varchar(60) );")
    con.commit()
    
def fill_vacancy(cur, con, vacancy_name, company, salary, city, url):
    cur.execute("INSERT INTO vacancy (vacancy_name, company, salary, city, url) VALUES ('{vacancy_name}', '{company}', '{salary}', '{city}', '{url}')".\
                format(vacancy_name=vacancy_name, company=company, salary=salary, city=city, url=url))
    con.commit()    
    

def db_tgid(tg_id, cur, con):
    cur.execute("SELECT * FROM user WHERE tg_id='{tg_id}'".\
                format(tg_id=tg_id))
    
    records = cur.fetchall()
    
    if not records:
        cur.execute("INSERT INTO user (tg_id) VALUES ('{tg_id}')".\
                    format(tg_id=tg_id)) 
        con.commit()
    else:
        con.commit()

def db_takevacancy(cur, con):
    cur.execute("SELECT * FROM vacancy")
    records = cur.fetchall()
    return records
    