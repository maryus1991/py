from typing import Counter, List
from selenium import webdriver
from datetime import datetime
import time as Time
import mysql.connector
from bs4 import BeautifulSoup


driver = webdriver.Firefox(executable_path='/home/maryus/Desktop/nothing/py/teacher_warning/geckodriver')
driver.get('https://web.shad.ir/')

distance_time_between_sending_massage_in_min = 30 
teacher_name_list = []
grope_name_list = ['شبکه آموزشی دانش آموز (شاد) ', 'FATEMEH','MOHAMMAD KAZEM',
'AMINNEBY'

]

db_host = 'localhost'
db_database = 'test'
db_user = 'test'
db_password = '1234'
def db_controller(db_command, selecting = False ,
                    db_host = db_host, db_user = db_user , 
                    db_password = db_password, db_database = db_database):

    mainDB = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        database = db_database
    )
    db_cursor = mainDB.cursor()
    if selecting :
        db_cursor.execute(db_command)
        db_result = db_cursor.fetchone()
        return db_result
    else :
        db_cursor.execute(db_command)
        mainDB.commit()
        return True

def get_localstorage():
    _localstorage_ = driver.execute_script("window.localStorage;")
    return _localstorage_

def localstorage_editing(): 
    x = r'"FhjfjAC5JxdJju0nE2I3Y8RIktjsqrXgEgY3T4eccMFps/pMTG/J6KtBr5rSEDj+"'
    f = f"window.localStorage.setItem('auth', '{x}')"
    driver.execute_script(f)
    driver.execute_script(f)
    # driver.refresh()

def element_finder_by_class_name(class_name):
    elem_list = driver.find_elements_by_class_name(class_name)
    return elem_list

def massage_sender(message):
    pass

def time_checker_for_massage(massage_sended_time):
    now_time = Time.time()
    distance_time = now_time - massage_sended_time
    if distance_time >= 1800 :
        return True
    else :  
        return False

def db_saver(teacher_name, sended_time):
    db_command_as_string:str = f"INSERT INTO Massage_counter (teacher_name, time_sended_message) VALUES ({teacher_name}, sended_time)" 
    db_controller(db_command_as_string)


def db_returner():
    db_command_as_string:str = f"SELECT * FROM Massage_counter ORDER BY ID DESC LIMIT 1; "
    result = db_controller(db_command_as_string, selecting=True)
    return result

def time_checker_for_grope_and_teacher():
    pass

def main():
    localstorage_editing()
    localstorage_editing()
    localstorage_editing()
    localstorage_editing()
    print(get_localstorage())
    localstorage_editing()
    print(get_localstorage())
    hTML_list = []
    input('...')
    localstorage_editing()
    localstorage_editing()
    print(get_localstorage())
    input('...')

    counter = 0 
    while True:
        for element in element_finder_by_class_name('im_dialog'):
            element_html = element.get_attribute('innerHTML')
            html_parser = BeautifulSoup(element_html, "html.parser")
            number_of_massage = html_parser.find('span', {'class': 'im_dialog_badge'})
            name_of_grope = html_parser.find('div', {'class': 'im_dialog_peer'}).text
            if name_of_grope in grope_name_list and int(number_of_massage.text) > 0 :
                print('@',name_of_grope,'@','===>',number_of_massage.text)
                if name_of_grope in hTML_list:
                    pass
                elif name_of_grope not in hTML_list: 
                    hTML_list.append(name_of_grope)
                else:
                    pass
            else:
                pass

        # print(hTML_list)
        # print(counter)
        Time.sleep(1)
        # driver.refresh()

if __name__ == '__main__':
    main()

#