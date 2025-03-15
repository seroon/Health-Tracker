import json
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import *
import pickle
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

from functools import partial


class TaskManager:
    def __init__(self, root):
        self.scrollbar = None
        self.root = root
        self.root.title("Aplicație de Listă de Sarcini")
        self.root.geometry("500x450+750+250")
        self.root.config(bg="#C4DEF2")

        self.image_path = "C:\\Users\\ADRIAN\\PycharmProjects\\To_Do_List\\LOGO2.png"
        self.img = tk.PhotoImage(file=self.image_path)
        self.img = self.img.subsample(3, 3)
        self.image_label = tk.Label(root, image=self.img, bd=0)

        self.image_label.grid()
        self.sarcini = []
        self.sarcini = self.load_tasks()

        self.titlu_label = tk.Label(root, text="Listă de Sarcini", font=("Lucida Calligraphy", 28, "bold"),
                                    bg="#C4DEF2")
        self.titlu_label.grid(row=0, column=5000, columnspan=2, pady=10)

        self.label_titlu = tk.Label(root, text="Titlu:", height=2, width=30)
        self.label_titlu.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.label_titlu.place(x=20, y=350)

        self.entry_titlu = tk.Entry(root)
        self.entry_titlu.grid(row=0, column=1, pady=5)
        self.entry_titlu.place(x=300, y=350, width=350, height=35)

        self.label_descriere = tk.Label(root, text="Descriere:", height=2, width=30)
        self.label_descriere.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.label_descriere.place(x=20, y=400)

        self.entry_descriere = tk.Entry(root)
        self.entry_descriere.grid(row=1, column=1, pady=5)
        self.entry_descriere.place(x=300, y=400, height=35, width=350)

        self.label_data_limita = tk.Label(root, text="Deadline:", height=2, width=30)
        self.label_data_limita.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.label_data_limita.place(x=20, y=450)

        self.entry_data_limita = tk.Entry(root)
        self.entry_data_limita.grid(row=2, column=1, pady=5)
        self.entry_data_limita.place(x=300, y=450, height=35, width=350)

        # listasarcini
        self.lista_sarcini = tk.Listbox(root, selectmode=tk.SINGLE, height=20, width=200, font=("High Tower Text", 20),
                                        fg="white", bg="#104E8B")
        self.lista_sarcini.grid(row=4, column=50, columnspan=2, pady=5)
        self.scrollbar = Scrollbar(self.root, orient="vertical")
        self.scrollbarX = Scrollbar(self.root, orient="horizontal")
        self.lista_sarcini.config(yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollbarX.set)
        self.scrollbar.config(command=self.lista_sarcini.yview)
        self.scrollbarX.config(command=self.lista_sarcini.xview)
        self.scrollbar.place(x=1690, y=250, height=600)
        self.scrollbarX.grid(sticky=tk.EW)
        self.scrollbarX.place(x=701, y=850, width=1005)

        # butoane
        self.buton_adauga = tk.Button(root, text="Adaugă Sarcină", command=self.adauga_sarcina, width=24, height=2,
                                      font=("bold"))
        self.buton_adauga.grid(row=3, column=1, pady=5, sticky=tk.W)

        self.buton_sterge = tk.Button(root, text="Șterge Sarcină", command=self.sterge_sarcina, widt=24, height=2,
                                      font=("bold"))
        self.buton_sterge.grid(row=8, column=1, pady=5, sticky=tk.W)

        self.buton_editeaza = tk.Button(root, text="Editează Sarcină", command=self.editeaza_sarcina, widt=24, height=2,
                                        font=("bold"))
        self.buton_editeaza.grid(row=9, column=1, pady=5, sticky=tk.W)

        self.buton_finalizat = tk.Button(root, text="Marchează ca Finalizată", command=self.marcheaza_finalizat,
                                         widt=24, height=2, font=("bold"))
        self.buton_finalizat.grid(row=10, column=1, pady=5, sticky=tk.W)

        self.buton_sortare_titlu = tk.Button(root, text="Sortează după Titlu", command=self.sorteaza_dupa_titlu,
                                             widt=24, height=2, font=("bold"))
        self.buton_sortare_titlu.grid(row=100, column=1, pady=5, sticky=tk.W)

        self.buton_adauga.place(x=180, y=280)
        # logouri
        # gym
        self.image_path_gym = "C:\\Users\\ADRIAN\\PycharmProjects\\To_Do_List\\gym.png"
        self.img_gym = tk.PhotoImage(file=self.image_path_gym)
        self.img_gym = self.img_gym.subsample(2, 2)
        self.image_label_gym = tk.Label(root, image=self.img_gym, bd=0)
        self.image_label_gym.grid()
        self.image_label_gym.place(x=1710, y=220)
        # groceries
        self.image_path_groce = "C:\\Users\\ADRIAN\\PycharmProjects\\To_Do_List\\cos.png"
        self.img_groce = tk.PhotoImage(file=self.image_path_groce)
        self.img_groce = self.img_groce.subsample(6, 6)
        self.image_label_groce = tk.Label(root, image=self.img_groce, bd=0)
        self.image_label_groce.grid()
        self.image_label_groce.place(x=1710, y=450)
        # minge
        self.image_path_ball = "C:\\Users\\ADRIAN\\PycharmProjects\\To_Do_List\\ball.png"
        self.img_ball = tk.PhotoImage(file=self.image_path_ball)
        self.img_ball = self.img_ball.subsample(6, 6)
        self.image_label_ball = tk.Label(root, image=self.img_ball, bd=0)
        self.image_label_ball.grid()
        self.image_label_ball.place(x=1730, y=320)
        # citit
        self.image_path_citit = "C:\\Users\\ADRIAN\\PycharmProjects\\To_Do_List\\citit.png"
        self.img_citit = tk.PhotoImage(file=self.image_path_citit)
        self.img_citit = self.img_citit.subsample(6, 6)
        self.image_label_citit = tk.Label(root, image=self.img_citit, bd=0)
        self.image_label_citit.grid()
        self.image_label_citit.place(x=1740, y=620)
        # caine
        self.image_path_caine = "C:\\Users\\ADRIAN\\PycharmProjects\\To_Do_List\\caine.png"
        self.img_caine = tk.PhotoImage(file=self.image_path_caine)
        self.img_caine = self.img_caine.subsample(6, 6)
        self.image_label_caine = tk.Label(root, image=self.img_caine, bd=0)
        self.image_label_caine.grid()
        self.image_label_caine.place(x=1730, y=750)

        self.buton_sortare_titlu.place(x=200, y=760)
        self.buton_sterge.place(x=200, y=830)
        self.buton_finalizat.place(x=200, y=620)
        self.buton_editeaza.place(x=200, y=690)
        self.image_label.place(x=30, y=20)

        self.lista_sarcini.place(x=700, y=250, width=1000, height=600)
        self.titlu_label.place(x=700, y=200)
        self.notification_thread = threading.Thread(target=self.check_deadlines, daemon=True)
        self.notification_thread.start()
        self.populate_listbox()

    def create_search_widgets(self):
        self.label_cautare = tk.Label(self.root, text="Caută Sarcină:", height=2, width=30)
        self.label_cautare.place(x=20, y=500)

        self.entry_cautare = tk.Entry(self.root)
        self.entry_cautare.place(x=300, y=500, height=35, width=350)

        self.buton_cautare = tk.Button(self.root, text="Caută", command=self.cauta_sarcina, width=24, height=2,
                                       font=("bold"))
        self.buton_cautare.place(x=200, y=550)

    def cauta_sarcina(self):
        termen_cautat = self.entry_cautare.get().lower()
        self.lista_sarcini.delete(0, tk.END)

        for sarcina in self.sarcini:
            if termen_cautat in sarcina['title'].lower():
                self.lista_sarcini.insert(tk.END,
                                          f"{sarcina['title']} - {sarcina['description']} - {sarcina['status']}")

    def adauga_sarcina(self):
        titlu = self.entry_titlu.get()
        descriere = self.entry_descriere.get()
        data_limita = self.entry_data_limita.get()

        self.entry_titlu.delete(0, tk.END)
        self.entry_descriere.delete(0, tk.END)
        self.entry_data_limita.delete(0, tk.END)

        self.salvare_sarcini(titlu, descriere, data_limita)
        self.populate_listbox()
        self.save_tasks()

    def check_deadlines(self):
        while True:
            for task in self.sarcini:
                if task['deadline'] and task['status'] == 'Necompletata':
                   self.show_notification(task)
            threading.Event().wait(24 * 60 * 60)

    def show_notification(self, task):
        if task['deadline'] < datetime.now().date():
            message = f"Sarcina '{task['title']}' este trecută de termen!"
        elif task['deadline'] == datetime.now().date():
            message = f"Sarcina '{task['title']}' are termenul limită astăzi!"
        else:
            message = f"Sarcina '{task['title']}' are termenul limita pana pe {task['deadline']}"

        messagebox.showinfo("Notificare", message)

    def sterge_sarcina(self):
        selected_indices = self.lista_sarcini.curselection()
        if not selected_indices:
            messagebox.showinfo("Informație", "Nicio sarcină selectată")
            return
        selected_index = selected_indices[0]
        response = messagebox.askokcancel("Informație", "Sunteti sigur ca vreti sa stergeti activitatea?")
        # Ștergerea sarcinii din lista internă și din widget-ul Listbox
        if response:
            del self.sarcini[selected_index]
            self.lista_sarcini.delete(selected_index)

            # Salvarea listei actualizate de sarcini
            self.save_tasks()

    def marcheaza_finalizat(self):
        selected_indices = self.lista_sarcini.curselection()
        if not selected_indices:
            messagebox.showinfo("Informație", "Nicio sarcină selectată")
            return
        selected_index = selected_indices[0]

        # Obținerea sarcinii și verificarea stării acesteia
        sarcina_selectata = self.sarcini[selected_index]
        if sarcina_selectata['status'] == 'Necompletata':
            sarcina_selectata['status'] = 'Îndeplinita'
            self.lista_sarcini.itemconfig(selected_index, {'bg': 'light green'})

            # Actualizarea listei și salvarea modificărilor
            self.populate_listbox()
            self.save_tasks()
        else:
            messagebox.showinfo("Informație", "Această sarcină a fost deja finalizată")

    def editeaza_sarcina(self):
        try:
            selected_index = self.lista_sarcini.curselection()[0]
            text_sarcina = self.lista_sarcini.get(selected_index)
            titlu = simpledialog.askstring("Editare Titlu", "Introduceți noul titlu:",
                                           initialvalue=text_sarcina.split("|")[0].strip().replace("Titlu:", ""))
            if titlu is not None:
                self.lista_sarcini.delete(selected_index)
                self.lista_sarcini.insert(selected_index,
                                          f" {titlu} |  {text_sarcina.split('|')[1].strip()} | Deadline: {text_sarcina.split('|')[2].strip()} | Stare: Necompletată")
                self.sarcini[selected_index] = self.lista_sarcini.get(selected_index)
                self.salvare_sarcini()
        except IndexError:
            pass

    def sorteaza_dupa_titlu(self):
        sarcini_sortate = sorted(self.sarcini, key=lambda x: x['title'].strip())

        # Șterge conținutul listei existente
        self.lista_sarcini.delete(0, tk.END)

        for sarcina in sarcini_sortate:
            self.lista_sarcini.insert(tk.END, f"{sarcina['title']} -{sarcina['description']}-{sarcina['status']}")

    def salvare_sarcini(self, title, description, deadline):
        if not title:
            messagebox.showwarning("Avertisment", "Titlul sarcinii nu poate fi gol!")
            return
        elif not description:
            messagebox.showwarning("Avertisment", "Descrierea sarcinii nu poate fi goala!")
            return
        elif not deadline:
            messagebox.showwarning("Avertisment", "Termenul limita al sarcinii trebuie introdus!")
            return

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None
        except ValueError:
            messagebox.showwarning("Avertisment", "Format de dată invalid. Utilizați YYYY-MM-DD.")
            return

        task = {"title": title, "description": description, "deadline": deadline_date, "status": "Necompletata"}
        self.sarcini.append(task)
        self.populate_listbox()
        self.show_notification(task)

    def populate_listbox(self):
        self.lista_sarcini.delete(0, tk.END)

        for sarcina in self.sarcini:
            sarcina_text = f"{sarcina['title']} - {sarcina['description']} - {sarcina['status']}"

            self.lista_sarcini.insert(tk.END, sarcina_text)
            if sarcina['status'] == 'Îndeplinita':
                self.lista_sarcini.itemconfig(self.lista_sarcini.size() - 1, {'bg': 'light green'})

    def save_tasks(self):
        with open("tasks.pkl", "wb") as file:
            pickle.dump(self.sarcini, file)

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as file:
                sarcini = pickle.load(file)
        except (EOFError, FileNotFoundError):
            sarcini = []
        return sarcini


if __name__ == "__main__":
    def check_login(username, password):
        return username == "admin" and password == "password"


def on_login_button_click():
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    if check_login(entered_username, entered_password):
        root.deiconify()
        login_window.withdraw()
        app = TaskManager(root)
        app.create_search_widgets()
    else:
        messagebox.showerror("Eroare de autentificare", "Utilizator sau parolă incorecte")


root = tk.Tk()
root.title("Aplicație Principală")


root.withdraw()


login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("500x500")


name_label=tk.Label(login_window, text="Utilizator:",font=("Arial", 14, "bold"))
name_label.pack()

titlu_label=tk.Label(login_window, text="Bine ati revenit!",fg="#00008B",font=("Arial", 24,"bold" ))
titlu_label.pack()

username_entry = tk.Entry(login_window, font=("Arial", 14))

username_entry.pack()

password_label=tk.Label(login_window, text="Parolă:",font=("Arial", 14, "bold"))
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()


login_button = tk.Button(login_window, text="Login",bg="#00008B",fg="white", command=on_login_button_click, font=("Arial",14,"bold"))
login_button.pack()

#pozitionarea pentru labeluri
titlu_label.place(x=140,y=30)
name_label.place(x=80,y=150)
username_entry.place(x=190,y=150,width=200,height=30)
password_label.place(x=80,y=200)
password_entry.place(x=190,y=200,width=200,height=30)
login_button.place(x=200,y=250,width=80,height=30)


root.config()
root.mainloop()
