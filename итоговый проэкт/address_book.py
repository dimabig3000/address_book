import os
import sqlite3
import tkinter as tk
from tkinter import ttk

# Создание базы данных и таблицы контактов
class ContactsDatabase:
    def __init__(self):
        # Устанавливаем соединение с базой данных
        self.connection = sqlite3.connect('contacts.db')
        self.cursor = self.connection.cursor()

        # Создаем таблицу "contacts", если она не существует
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT
        )""")
        
        self.connection.commit()

contacts_db = ContactsDatabase()

# Функция для отображения контактов в таблице
def display_contacts():
    # Очищаем таблицу от существующих записей
    for row in contacts_tree.get_children():
        contacts_tree.delete(row)

    # Получаем контакты из базы данных и отображаем их в таблице
    contacts_db.cursor.execute('SELECT * FROM contacts')
    contacts = contacts_db.cursor.fetchall()
    for contact in contacts:
        contacts_tree.insert('', 'end', values=contact)

# Функция для добавления контакта
def add_contact():
    def save_contact():
        # Получаем данные из полей ввода
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        # Вставляем новый контакт в базу данных
        contacts_db.cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
        contacts_db.connection.commit()

        # Обновляем отображение контактов и закрываем окно добавления
        display_contacts()
        add_window.destroy()

    # Создаем окно для добавления контакта
    add_window = tk.Toplevel(root)
    add_window.title('Добавить контакт')

    # Добавляем элементы управления на окно
    name_label = tk.Label(add_window, text='Имя:')
    name_entry = tk.Entry(add_window)
    phone_label = tk.Label(add_window, text='Телефон:')
    phone_entry = tk.Entry(add_window)
    email_label = tk.Label(add_window, text='Email:')
    email_entry = tk.Entry(add_window)
    save_button = tk.Button(add_window, text='Сохранить', command=save_contact)

    name_label.pack()
    name_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    email_label.pack()
    email_entry.pack()
    save_button.pack()

# Функция для обновления контакта
def update_contact():
    def save_contact():
        # Получаем данные из полей ввода
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        # Обновляем контакт в базе данных
        selected_item = contacts_tree.selection()[0]
        selected_id = contacts_tree.item(selected_item)['values'][0]
        contacts_db.cursor.execute('UPDATE contacts SET name=?, phone=?, email=? WHERE id=?', (name, phone, email, selected_id))
        contacts_db.connection.commit()

        # Обновляем отображение контактов и закрываем окно обновления
        display_contacts()
        update_window.destroy()

    # Получаем выделенный контакт
    selected_item = contacts_tree.selection()[0]
    selected_id = contacts_tree.item(selected_item)['values'][0]

    # Получаем данные о контакте из базы данных
    contacts_db.cursor.execute('SELECT * FROM contacts WHERE id=?', (selected_id,))
    contact = contacts_db.cursor.fetchone()

    # Создаем окно для обновления контакта
    update_window = tk.Toplevel(root)
    update_window.title('Обновить контакт')

    # Добавляем элементы управления на окно
    name_label = tk.Label(update_window, text='Имя:')
    name_entry = tk.Entry(update_window)
    name_entry.insert(0, contact[1])
    phone_label = tk.Label(update_window, text='Телефон:')
    phone_entry = tk.Entry(update_window)
    phone_entry.insert(0, contact[2])
    email_label = tk.Label(update_window, text='Email:')
    email_entry = tk.Entry(update_window)
    email_entry.insert(0, contact[3])
    save_button = tk.Button(update_window, text='Сохранить', command=save_contact)

    name_label.pack()
    name_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    email_label.pack()
    email_entry.pack()
    save_button.pack()

# Функция для удаления контактов
def delete_contacts():
    for selected_item in contacts_tree.selection():
        selected_id = contacts_tree.item(selected_item)['values'][0]
        contacts_db.cursor.execute('DELETE FROM contacts WHERE id=?', (selected_id,))
        contacts_db.connection.commit()
        contacts_tree.delete(selected_item)

# Функция для поиска контактов
def search_contacts():
    def search_contact():
        search_text = search_entry.get()
        contacts_db.cursor.execute('SELECT * FROM contacts WHERE name LIKE ?', ('%' + search_text + '%',))
        contacts = contacts_db.cursor.fetchall()

        # Очищаем таблицу от существующих записей
        for row in contacts_tree.get_children():
            contacts_tree.delete(row)

        # Отображаем результаты поиска
        for contact in contacts:
            contacts_tree.insert('', 'end', values=contact)

        search_window.destroy()

    # Создаем окно для поиска контактов
    search_window = tk.Toplevel(root)
    search_window.title('Поиск контактов')

    # Добавляем элементы управления на окно
    search_label = tk.Label(search_window, text='Введите имя контакта:')
    search_entry = tk.Entry(search_window)
    search_button = tk.Button(search_window, text='Найти', command=search_contact)

    search_label.pack()
    search_entry.pack()
    search_button.pack()

# Функция для обновления данных в таблице
def refresh_table():
    display_contacts()

# Создание главного окна приложения
root = tk.Tk()
root.title('Телефонная книга')

# Создание верхней панели с кнопками
toolbar = tk.Frame(root)

# Создаем кнопки и добавляем их на верхнюю панель
add_picture = tk.PhotoImage(file='img/add.png')
add_button = tk.Button(toolbar, command=add_contact, image=add_picture)

update_picture = tk.PhotoImage(file='img/update.png')
update_button = tk.Button(toolbar, command=update_contact, image=update_picture)

delete_picture = tk.PhotoImage(file='img/delete.png')
delete_button = tk.Button(toolbar, command=delete_contacts, image=delete_picture)

search_picture = tk.PhotoImage(file='img/search.png')
search_button = tk.Button(toolbar, command=search_contacts, image=search_picture)

refresh_picture = tk.PhotoImage(file='img/refresh.png')
refresh_button = tk.Button(toolbar, command=refresh_table, image=refresh_picture)

add_button.pack(side=tk.LEFT)
update_button.pack(side=tk.LEFT)
delete_button.pack(side=tk.LEFT)
search_button.pack(side=tk.LEFT)
refresh_button.pack(side=tk.LEFT)

toolbar.pack(side=tk.TOP, fill=tk.X)

# Создание таблицы для отображения контактов
contacts_tree = ttk.Treeview(root, columns=('id', 'name', 'phone', 'email'), show='headings')
contacts_tree.heading('id', text='ID')
contacts_tree.heading('name', text='Имя')
contacts_tree.heading('phone', text='Телефон')
contacts_tree.heading('email', text='Email')
contacts_tree.column('id', width=50)
contacts_tree.column('name', width=150)
contacts_tree.column('phone', width=150)
contacts_tree.column('email', width=150)
contacts_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Отображение контактов в таблице
display_contacts()

# Запуск главного цикла приложения
root.mainloop()

# Закрытие базы данных
contacts_db.connection.close()
