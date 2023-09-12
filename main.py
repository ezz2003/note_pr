import csv
import datetime
import json
import re


def read_notes(file_name):
    '''
    чтение заметок из файла
    :param file_name: str имя файла.json
    :return: list of dict
    '''
    with open(file_name, 'r') as f:
        notes = json.load(f)
    return notes


def save_notes_json(notes, file_name):
    '''
    сохранение заметок в файл json
    :param notes: list of dict
    :param file_name: str
    '''
    with open(file_name, 'w') as f:
        json.dump(notes, f)
    print("SAVED!")


def finde_notes_by_date(notes, date):
    '''
    извлечение заметок за определённую дату
    :param notes: list of dict список заметок
    :param date: date
    :return: list of dict - список заметок за заданную дату
    '''
    finded_notes = []
    for note in notes:
        note_date = datetime.datetime.strptime(note['timestamp'], '%Y-%m-%d %H:%M:%S.%f')  # ???
        if note_date.date() == date:
            finded_notes.append(note)
    return finded_notes


def print_notes(notes):
    '''
    Вывод в консоль выбранной записи или всего списка.
    Если список не пуст, перед выводом он сортируется по дате
    :param notes: list of dict список заметок
    '''
    if not notes:
        print("Заметок не найдено")
    else:
        # notes = sorted_notes_by_date(notes)
        for note in notes:
            print(f'ID: {note["id"]}')
            print(f'Title: {note["title"]}')
            print(f'Text: {note["body"]}')
            print(f'Date/Time: {note["timestamp"]}')
            print()
        print(f'Всего найдено {len(notes)} заметок.')


def sorted_notes_by_date(notes):
    '''
    сортирует список заметок по дате издания
    :param notes: list of dict список заметок
    :return: list of dict сортированный по дате издания список заметок
    '''
    filtered_notes = sorted(notes, key=lambda d: d['timestamp'], reverse=False)
    print('\nSORTED!')
    return filtered_notes


def add_note(notes):
    '''
    Добавление новой записи
    :param notes: list of dict список заметок
    :return: list of dict список заметок с добавленной новой заметкой
    '''
    id = len(notes) + 1
    title = input("Введите заголовок: ")
    body = input("Введите тело заметки: ")
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    new_note = {'id': id, 'title': title, 'body': body, 'timestamp': timestamp}
    notes.append(new_note)
    return notes


def edit_note(notes, id):
    '''
    функция для редактирования заметки
    запрашивает новые данные и сохраняет в файл
    :param notes: list of dict список заметок
    :param id: int ID зааметки, которую редактировать
    :return: list of dict редактированный список заметок
    '''
    for note in notes:
        if note['id'] == id:
            note['title'] = input(f'Введите заголовок. Старый заголовок - {note["title"]}: ')
            note['body'] = input(f'Введите новое тело заметки. Старое тело заметки - {note["body"]}: ')
            note['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            return notes
    print(f'\nЗаметки с ID = {id} не найдено.')
    return notes


def delete_note(notes, id):
    '''
    функция удаления записи из списка записей
    :param notes: list of dict список заметок
    :param id: int ID - id записи, которую удалить
    :return: list of dict список заметок без записи, которую удалили
    '''
    for note in notes:
        if note['id'] == id:
            notes.remove(note)
            return notes
    print(f'\nЗаметки с ID = {id} не найдено.')


file_name = "notes.json"
try:
    notes = read_notes(file_name)
except:
    notes = []
    save_notes_json(notes, file_name)

flag = True
while flag:
    print('\n1. Вывести все заметки.\t\t\t\t 2. Вывести все заметки за Дату.')
    print('3. Вывести конкретную заметку.\t\t 4. Добавить новую заметку.')
    print('5. Редактировать заметку. \t\t\t 6. Удалить заметку.')
    print('7. Удалить все заметки.\t\t\t\t 8. Сортировать заметки по дате издания.')
    print('0. Выход из программы.\n')

    choice = str(input('Выберите команду: '))

    match choice:
        case '1':
            print_notes(notes)
        case '2':
            date_pattern = "\d{4}-\d{2}-\d{2}"
            date_str = input(('Введите дату в формате ГГГ-ММ-ДД: '))
            if (re.match(date_pattern, date_str) is not None):
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                filtered_notes = finde_notes_by_date(notes, date)
                print_notes(filtered_notes)
            else:
                print("\nНе установлен формат введённой даты")
        case '3':
            id = int(input('Введите ID заметки: '))
            note = [note for note in notes if note['id'] == id]
            print_notes(note)
        case '4':
            notes = add_note(notes)
            save_notes_json(notes, file_name)
        case '5':
            id = int(input('Введите ID заметки для редактирования: '))
            notes = edit_note(notes, id)
            save_notes_json(notes, file_name)
        case "6":
            id = int(input('Введите ID заметки для удаления: '))
            notes = delete_note(notes, id)
            save_notes_json(notes, file_name)
        case "7":
            notes = []
            save_notes_json(notes, file_name)
        case '8':
            sorted_notes_by_date(notes)
            save_notes_json(notes, file_name)
        case '0':
            print('BYE!')
            flag = False
        case _:
            print("Не известная команда")
