from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from pprint import pformat
import requests, json
from threading import Thread
import sys
import os

s = requests.Session()
headers2 = {'Content-type': 'text/html'}

def open():
    flag = True
    open2(flag)

def open2(flag):
    def search_items(item):
        global d
        d = {}
        sklads_url = f'https://inside.oooeidos.ru/api/v1/nodes/i/{item}/warehouses_balance'
        sklads = s.get(sklads_url, headers=headers2)
        sklads_text = json.loads(sklads.text)
        for i in range(len(sklads_text)):
            if sklads_text[i]['quantity'] != '0.0':
                d[sklads_text[i]['name']] = sklads_text[i]['quantity']
        if d == {}:
            d = ' На складах: Числится 0!'



    def search_supnodes(item):
        global b
        b = {}
        material_url = f'https://inside.oooeidos.ru/api/v1/nodes/i/{item}'
        material = s.get(material_url, headers=headers2)
        material_text = json.loads(material.text)
        if material_text['node_result']['is_material']:
            supnodes_url = f'https://inside.oooeidos.ru/api/v1/nodes/i/{item}/using_this_material_in_items'
            supnodes = s.get(supnodes_url, headers=headers2)
            supnodes_text = json.loads(supnodes.text)
            for i in range(len(supnodes_text)):
                a_id = supnodes_text[i]['item_id']
                a_quant = supnodes_text[i]['quantity']
                a_url = f'https://inside.oooeidos.ru/api/v1/nodes/i/{a_id}/warehouses_balance'
                a = s.get(a_url, headers=headers2)
                a_text = json.loads(a.text)
                flag = False
                c = {}
                if a.text != '[]':
                    for i in range(len(a_text)):
                        if a_text[i]['quantity'] != '0.0':
                            flag = True
                        if flag == True:
                            for i in range(len(a_text)):
                                if a_text[i]['quantity'] != '0.0':
                                    c[a_text[i]['name']] = a_text[i]['quantity']
                            b[f"i{a_id} - {a_quant} шт."] = [c]
            if b == {}:
                b = ' На складах: Числится 0!'
        else:
            supnodes_url = f'https://inside.oooeidos.ru/api/v1/nodes/i/{item}/supnodes'
            supnodes = s.get(supnodes_url, headers=headers2)
            supnodes_text = json.loads(supnodes.text)
            for i in range(len(supnodes_text)):
                a_id = supnodes_text[i]['p_id']
                a_quant = supnodes_text[i]['quantity']
                a_url = f'https://inside.oooeidos.ru/api/v1/nodes/a/{a_id}/warehouses_balance'
                a = s.get(a_url, headers=headers2)
                a_text = json.loads(a.text)
                flag = False
                c = {}
                if a.text != '[]':
                    for i in range(len(a_text)):
                        if a_text[i]['quantity'] != '0.0':
                            flag = True
                        if flag == True:
                            for i in range(len(a_text)):
                                if a_text[i]['quantity'] != '0.0':
                                    c[a_text[i]['name']] = a_text[i]['quantity']
                            b[f"a{a_id} - {a_quant} шт."] = [c]
            if b == {}:
                b = ' На складах: Числится 0!'


    def search_products(item):
        global h
        h = {}
        products_url = f'https://inside.oooeidos.ru/api/v1/nodes/i/{item}/product_list'
        products = s.get(products_url, headers=headers2)
        products_text = json.loads(products.text)
        for j in range(len(products_text)):
            products_id = products_text[j]['id']
            product_url = f'https://inside.oooeidos.ru/api/v1/nodes/a/{products_id}/warehouses_balance'
            product = s.get(product_url, headers=headers2)
            product_text = json.loads(product.text)
            flag = False
            g = {}
            if product.text != '[]':
                for i in range(len(product_text)):
                    if product_text[i]['quantity'] != '0.0':
                        flag = True
                    if flag == True:
                        for i in range(len(product_text)):
                            if product_text[i]['quantity'] != '0.0':
                                g[product_text[i]['name']] = product_text[i]['quantity']
                        h[f"a{products_id} - {products_text[j]['name']}"] = [g]


    def search_info(item):
        global g
        g = ''
        info_url = f'https://inside.oooeidos.ru/api/v1/nodes/i/{item}'
        info = s.get(info_url, headers=headers2)
        info_text = json.loads(info.text)
        g = info_text['node_result']['name']


    def search2():
        flag = True
        search(flag)


    def search(flag):
        item = ids.get()
        if item == '':
            messagebox.showinfo('Ошибка Ввода', 'Введите айди для поиска!')
        else:
            s_items = Thread(target=search_items, args=(item,))
            s_supnodes = Thread(target=search_supnodes, args=(item,))
            s_products = Thread(target=search_products, args=(item,))
            s_info = Thread(target=search_info, args=(item,))
            s_products.start()
            s_supnodes.start()
            s_items.start()
            s_info.start()
            s_products.join()
            s_supnodes.join()
            s_items.join()
            s_info.join()

            sklad_text = ScrolledText(window2, width=25, height=37)
            sklad_text.place(x=10, y=30)
            sklad_text.insert(1.0, pformat(d).replace("'", "").replace("[", " ").replace("]", "").replace("{", " ", 1)[:-1])
            sklad_text.configure(state=DISABLED)
            supnodes_text = ScrolledText(window2, width=80, height=37)
            supnodes_text.place(x=238, y=30)
            supnodes_text.insert(1.0, pformat(b).replace("'", "").replace("[", " ").replace("]", "").replace("{", " ", 1)[:-1])
            supnodes_text.configure(state=DISABLED)
            product_text = ScrolledText(window2, width=97, height=37)
            product_text.place(x=908, y=30)
            product_text.insert(1.0, pformat(h).replace("'", "").replace("[", " ").replace("]", "").replace("{", " ", 1)[:-1])
            product_text.configure(state=DISABLED)
            info = Text(window2, width=17, height=10, wrap='word', bd=0, bg="#1A2738", fg="white", font=("None", 12, "bold"))
            info.place(x=1720, y=125)
            info.insert(1.0, pformat(g).replace("'", "")[:-1])
            info.configure(state=DISABLED)


    if login.get() == '' and passw.get() == '':
        messagebox.showinfo('Ошибка Авторизации', 'Введите данный для входа!')
    elif passw.get() == '':
        messagebox.showinfo('Ошибка Авторизации', 'Введите пароль!')
    else:
        status = connect(login.get(), passw.get())
        if status != 200:
            messagebox.showinfo('Ошибка Авторизации', 'Неправильный пароль или логин!')
        else:
            window.destroy()
            window2 = Tk()
            window2.iconbitmap(iconPath)
            window2.title('Поиск остатков деталей')
            window2.geometry('1900x640+0+100')
            window2.maxsize(1900, 640)
            window2.config(bg='#1A2738')
            sklad = Label(window2, text='На складах / в отделах', font=75, bg="#1A2738", fg="white")
            sklad.place(x=25, y=5)
            supnodes = Label(window2, text='Список сборок, где есть деталь', font=75, bg="#1A2738", fg="white")
            supnodes.place(x=450, y=5)
            products = Label(window2, text='Готовая продукция, в которой есть эта деталь', font=75, bg="#1A2738", fg="white")
            products.place(x=1150, y=5)
            lbl = Label(window2, text='Введите Айди\nкоторая вас интересует', font=75, bg="#1A2738", fg="white")
            lbl.place(x=1715, y=5)
            ids = Entry(window2, width=11, font=25)
            ids.place(x=1766, y=50)
            btn = Button(window2, text='Найти', font=50, command=search2, bg='#374351', fg='white')
            btn.place(x=1786, y=76)
            if flag:
                window2.bind("<Return>", search)
            window2.mainloop()


def connect(user, passw):
    url = 'https://inside.oooeidos.ru/login.json'
    data = {
        'username': user,
        'password': passw
    }
    headers = {'Content-type': 'application/json'}
    conn = s.post(url, data=json.dumps(data), headers=headers)
    return conn.status_code


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

global flag
flag = False
window = Tk()
iconPath = resource_path('my.ico')
window.iconbitmap(iconPath)
window.title("Поиск остатков деталей")
window.geometry('275x120+800+400')
window.maxsize(275,120)
window.config(bg= "#141F2D")
lbl = Label(window, text="Вход на сайт Redmine", font=75, bg="#141F2D", fg="white")
lbl.pack(side=TOP, pady=2)
login_text = Label(window, text="Логин:", font=50, bg="#141F2D", fg="white")
login_text.place(x=5, y=27)
login = Entry(window, width=20, font=25)
login.place(x=80, y=29)
passw_text = Label(window, text="Пароль:", font=50, bg="#141F2D", fg="white")
passw_text.place(x=5, y=52)
passw = Entry(window, text='Логин', width=20, font=25, show='*')
passw.place(x=80, y=54)
btn = Button(window, text="Вход", font=50, command=open, bg='#374351', fg='white')
btn.place(x=115, y=82)
if flag == False:
    window.bind("<Return>", open2)
window.mainloop()
