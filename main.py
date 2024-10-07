from tkinter import *
from os import mkdir
import os
from tkinter import messagebox
from tkcalendar import DateEntry
from customtkinter import *
from tkinter import ttk

path = os.getcwd()
day_list = list()


#Crear el usuario
def create():
    # Determina si el usuario introdujo un nombre
    if len(create_entry.get()) == 0 or len(create_pwd_entry.get()) == 0:
        messagebox.showerror(title="ERROR", message="Rellene los campos necesarios")
    elif len(create_pwd_entry.get()) < 8:
        messagebox.showerror(title="ERROR", message="Su contraseña debe contener al menos 8 caracteres")
    else:
        directory = create_entry.get().title()
        password = create_pwd_entry.get()
        x.set("")
        c.set("")

        try:
            # Crea la carpeta relativa al usuario
            mkdir(f"{directory}")
            try:
                # Crea los archivos globales correspondientes al usuario
                file = open(f"{path}\\{directory}\\Ganancias.txt", "x")
                file.close()
                file_2 = open(f"{path}\\{directory}\\Gastos.txt", "x")
                file_2.close()
                file_3 = open(f"{path}\\{directory}\\pwd.txt", "x")
                file_3.write(password)
                file_3.close()
                file_4 = open(f"{path}\\{directory}\\Days.txt", "x")
                file_4.close()
                messagebox.showinfo(title="Éxito", message="Usuario creado con éxito")
            except:
                messagebox.showerror(title="Error", message="Ocurrió algo inesperado")
        # En caso de que exista ese nombre de usuario
        except FileExistsError:
            messagebox.showerror(title="Error", message="Ese nombre de usuario ya existe")


# Acceder a los datos del usuario
def user():

    try:
        #Comprobar la contraseña
        directory = user_entry.get().title()
        file_0 = open(f"{path}\\{directory}\\pwd.txt", "r")
        password = file_0.read()
        file_0.close()

        # Determinar si se ha introducido un nombre de usuario
        if len(user_entry.get()) == 0 or len(password_entry.get()) == 0:
            messagebox.showerror(title="ERROR", message="Rellene los campos necesarios")
        elif password_entry.get() != password:
            messagebox.showerror(title="ERROR", message="Contraseña incorrecta")
        else:

            file_d = open(f"{path}\\{directory}\\Days.txt", "r")
            for line in file_d:
                day_list.append(line)
            file_d.close()

            view_data()
            view()

            user_entry.configure(state="disabled")
            add_expense.configure(state="normal")
            view_info.configure(state="normal")
            add_income.configure(state="normal")
            p.set("")
            password_entry.configure(state="disabled")

    except FileNotFoundError:
        messagebox.showerror(title="ERROR", message="Ese nombre de usuario no existe")


# Cambiar de usuario
def change():
    password_entry.configure(state="normal")
    user_entry.configure(state="normal")
    u.set("")
    add_expense.configure(state="disabled")
    add_income.configure(state="disabled")
    income_report.configure(state="normal")
    income_report.delete("1.0", END)
    income_report.configure(state="disabled")
    expenses_report.configure(state="normal")
    expenses_report.delete("1.0", END)
    expenses_report.configure(state="disabled")
    e.set("")
    i.set("")
    s.set("")


# Ventana para introducir gastos o ingresos
def boton(testo):

    new_window = CTkToplevel()
    new_window.attributes('-topmost', True)
    new_window.resizable(False, False)

    new_wtotal = new_window.winfo_screenwidth()
    new_htotal = new_window.winfo_screenheight()
    new_wventana = 260
    new_hventana = 120

    new_pwidth = round(new_wtotal / 2 - new_wventana / 2)
    new_pheight = round(new_htotal / 2 - new_hventana / 2)

    new_window.geometry(str(new_wventana) + "x" + str(new_hventana) + "+" + str(new_pwidth) + "+" + str(new_pheight))

    if testo == 'add':
        action = "ingreso"
        file_name = "Ingresos"
        result = "Ganancias"
    elif testo == 'remove':
        action = "gasto"
        file_name = "Gastos"
        result = "Gastos"
    lab = StringVar()

    descripcion = CTkLabel(new_window, text="Descripción: ", font=("Comic Sans MS", 20))
    descripcion.grid(row=0, column=0)
    des = CTkEntry(new_window, font=("Arial", 20))
    des.grid(row=0, column=1)
    cant = CTkLabel(new_window, text="Cantidad: ", font=("Comic Sans MS", 20))
    cant.grid(row=1, column=0)
    cantidad = CTkEntry(new_window, font=("Arial", 20))
    cantidad.grid(row=1, column=1)
    aceptar = CTkButton(new_window, text="Añadir", font=("Comic Sans MS", 20),
                        command=lambda: add(des.get(), cantidad.get(), action, file_name, result, new_window, lab))
    aceptar.grid(row=2, columnspan=2)
    error_label = CTkLabel(new_window, textvariable=lab)
    error_label.grid(row=3, columnspan=2)


# Añadir ingresos
def add(mot, cant, action, file_name, result, new_window, lab):

    motive = mot
    ammount = cant
    day = date.get()
    day = day.replace("/", "-")
    name = user_entry.get().title()

    # Confirmar que quiere añadir el gasto/ingreso
    if len(motive) == 0 or len(ammount) == 0:
        lab.set("Debes rellenar todos los campos")
    elif not ammount.isnumeric():
        lab.set("Debes introducir una cantidad válida")
    else:
        new_window.destroy()

        # Crear la carpeta relativa a la fecha en caso de que no exista
        try:
            mkdir(f"{path}\\{name}\\{day}")
        except FileExistsError:
            pass

        # Crear el archivo donde se guardarán los ingresos relativos al día seleccionado en caso de no existir
        try:
            file_2 = open(f"{path}\\{name}\\{day}\\{file_name}.txt", "x")
            file_2.write(f"{file_name} del día {day}:")
            file_2.close()

            apnd = True

            for i in day_list:
                if i == day:
                    apnd = False
            if apnd is True:
                day_list.append(day.rstrip("\n"))
                day_list.sort()

            file_d = open(f"{path}\\{name}\\Days.txt", "w")
            for i in day_list:
                file_d.write(i + "\n")
            file_d.close()

        except FileExistsError:
            pass
        except:
            messagebox.showerror(title="Error", message="Ocurrió algo inesperado")

        # Determinar si no hay errores por parte del usuario
        try:
            # añadir los ingresos al archivo correspondiente
            file = open(f"{path}\\{name}\\{day}\\{file_name}.txt", "a")
            file.write(f"\n{motive}: {ammount}")
            file.close()

            # añadir las ganancias al archivo global de ganancias
            file_3 = open(f"{path}\\{name}\\{result}.txt", "a")
            file_3.write(f"{motive}:{ammount}" + os.linesep)
            file.close()

            m.set("")
            n.set("")
        except:
            messagebox.showerror(message="Algo inesperado ocurrió", title="ERROR")

        # Actualizar la información mostrada
        file_3 = open(f"{path}\\{name}\\{result}.txt", "r")
        file_3.close()
        view_data()
        view()


def view_data():
    total_i = 0
    total_e = 0
    name = user_entry.get().title()

    try:
        # Muestra y calcula el total de ingresos
        file = open(f"{path}\\{name}\\Ganancias.txt", "r")
        for line in file:
            if line.startswith("\n"):
                pass
            else:
                total_i += int(line.split(":")[1].lstrip(' '))
        i.set(f"Ingresos totales: {total_i}")
        file.close()

        # Muestra y calcula el total de gastos
        file_2 = open(f"{path}\\{name}\\Gastos.txt", "r")
        for line in file_2:
            if line.startswith("\n"):
                pass
            else:
                total_e += int(line.split(":")[1].lstrip(' '))
        e.set(f"Gastos totales: {total_e}")
        file_2.close()

        currency = total_i - total_e
        s.set(f"Saldo: {currency}")

    except FileNotFoundError:
        messagebox.showerror(title="ERROR", message="No existe ninguna cuenta asociada a este usuario")


def view():
    income_report.configure(state="normal")
    expenses_report.configure(state="normal")

    total_income = 0
    total_expenses = 0
    day = date.get()
    day = day.replace("/", "-")
    name = user_entry.get().title()

    # abrir el archivo que contiene los ingresos
    try:
        with open(f"{path}\\{name}\\{day}\\Ingresos.txt", "r") as file:
            income_report.delete("1.0", END)
            for line in file:
                # Mostrar el contenido del archivo
                income_report.insert(END, str(line)+"\n")
                # Determinar la cantidad total de ingresos del día
                if not line.startswith('Ingresos del'):
                    money_ammount = int(line.split(":")[1].lstrip(' '))
                    total_income += money_ammount
                else:
                    pass
        total_income = str(total_income)
        income_report.insert(END, f"\n\nTotal: {total_income}")

    # En caso de que no haya ningún ingreso en el día seleccionado
    except FileNotFoundError:
        income_report.delete("1.0", END)
        income_report.insert("1.0", "No existen ingresos en el día seleccionado")

    # Abrir el archivo que contiene los gastos
    try:
        with open(f"{path}\\{name}\\{day}\\Gastos.txt", "r") as file_2:
            expenses_report.delete("1.0", END)
            # Mostrar el contenido del archivo seleccionado
            for line in file_2:
                expenses_report.insert(END, str(line)+"\n")
                # Determinar el total de gastos del día seleccionado
                if not line.startswith('Gastos del'):
                    money_ammount = int(line.split(":")[1].lstrip(' '))
                    total_expenses += money_ammount
                else:
                    pass
        total_expenses = str(total_expenses)
        expenses_report.insert(END, f"\n\nTotal: {total_expenses}")

    # En caso de que no existan gastos relativos al día seleccionado
    except FileNotFoundError:
        expenses_report.delete("1.0", END)
        expenses_report.insert("1.0", "No existen gastos en el día seleccionado")

    income_report.configure(state="disabled")
    expenses_report.configure(state="disabled")


def movement(name):
    try:

        file = open(f"{path}\\{name}\\Days.txt", "r") # Abrir el archivo donde se almacenan los días con movimiento

        lab = StringVar()
        list_of_days = list()

        new_window = CTkToplevel()
        new_window.attributes('-topmost', True)
        new_window.resizable(False, False)

        new_wtotal = new_window.winfo_screenwidth()
        new_htotal = new_window.winfo_screenheight()
        new_wventana = 260
        new_hventana = 120

        new_pwidth = round(new_wtotal / 2 - new_wventana / 2)
        new_pheight = round(new_htotal / 2 - new_hventana / 2)

        new_window.geometry(str(new_wventana) + "x" + str(new_hventana) + "+" + str(new_pwidth) + "+" + str(new_pheight))

        days_display = ttk.Combobox(new_window, height=10, width=100, state='readonly',
                                    font=('Arial', 15))

        # Agregar los nuevos días a la lista
        for line in file:
            if line.startswith("\n"):
                pass
            else:
                list_of_days.append(line.rstrip("\n"))
        list_of_days.sort()

        # Añadir los días al programa
        for d in list_of_days:
            values = list(days_display['values'])
            days_display['values'] = values + [d]

        days_display.set('Días con movimiento')
        days_display.pack(side="top")
        file.close()

        go_to = CTkButton(new_window, text='Ver movimiento', font=('Comic Sans MS', 20),
                          command=lambda:set_day(days_display.get().replace("-", "/"), new_window, lab))
        go_to.pack(side="bottom")

        error_label = CTkLabel(new_window, textvariable = lab)
        error_label.pack(side="bottom")

    except FileNotFoundError:
        messagebox.showerror(title="ERROR", message="No se ha seleccionado ningún usuario")


def set_day(day, new_window, lab):
    try:
        date.set_date(day)
        view()
        new_window.destroy()
    except ValueError:
        lab.set("Ningún día seleccionado")

window = CTk()

window.title("Mis cuentas")

wtotal = window.winfo_screenwidth()
htotal = window.winfo_screenheight()
wventana = 900
hventana = 720

#  Aplicamos la siguiente formula para calcular donde debería posicionarse
pwidth = round(wtotal / 2 - wventana / 2)
pheight = round(htotal / 2 - hventana / 2)

#  Se lo aplicamos a la geometría de la ventana
window.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))

m = StringVar()
n = StringVar()
x = StringVar()
u = StringVar()
s = StringVar()
e = StringVar()
i = StringVar()
p = StringVar()
c = StringVar()

frame = CTkFrame(window)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Opciones", menu=file_menu)
file_menu.add_command(label="Cambiar usuario", command=change, font=("Arial", 11))
file_menu.add_command(label="Ver días con movimiento", command=lambda : movement(user_entry.get().title()), font=("Arial", 11))

user_label = CTkLabel(frame, text="Usuario: ", font=('Comic Sans MS', 20))
user_label.grid(row=1, column=0)

user_entry = CTkEntry(frame, textvariable=u, font=('Arial', 15))
user_entry.grid(row=1, column=1)


password_label = CTkLabel(frame, text="Contraseña: ", font=('Comic Sans MS', 20))
password_label.grid(row=3, column=0)

password_entry = CTkEntry(frame, textvariable=p, font=('Arial', 15), show="*")
password_entry.grid(row=3, column=1)

user_button = CTkButton(frame, text="Aceptar", command=user, font=('Comic Sans MS', 20))
user_button.grid(row=3, column=2)


create_label = CTkLabel(frame, text="Crear nuevo usuario: ", font=('Comic Sans MS', 20))
create_label.grid(row=5, column=0)

create_entry = CTkEntry(frame, textvariable=x, font=('Arial', 15))
create_entry.grid(row=5, column=1)


create_pwd_label = CTkLabel(frame, text="Crear contraseña: ", font=("Comic Sans MS", 20))
create_pwd_label.grid(row=7, column=0)

create_pwd_entry = CTkEntry(frame, textvariable=c, font=('Arial', 15), show="*")
create_pwd_entry.grid(row=7, column=1)

create_button = CTkButton(frame, text="CREAR", command=create, font=('Comic Sans MS', 20))
create_button.grid(row=7, column=2)


date = DateEntry(frame, date_pattern='dd/mm/y', font=('Comic Sans MS', 15))
date.grid(row=9, column=0)

view_info = CTkButton(frame, text="Ver informe", command=view, state="disabled", font=('Comic Sans MS', 20))
view_info.grid(row=9, column=1)

add_income = CTkButton(frame, text="Añadir ingreso", command=lambda: boton("add"), state="disabled", font=('Comic Sans MS', 20))
add_income.grid(row=9, column=2)

add_expense = CTkButton(frame, text="Añadir gasto", command=lambda: boton("remove"), state="disabled", font=('Comic Sans MS', 20))
add_expense.grid(row=9, column=3)


money = CTkLabel(frame, text="Saldo: ", textvariable=s, font=('Comic Sans MS', 20))
money.grid(row=11, column=1, columnspan=2)

income = CTkLabel(frame, text="Ingresos totales: ", textvariable=i, font=('Comic Sans MS', 20))
income.grid(row=11, column=0)

expenses = CTkLabel(frame, text="Gastos totales: ", textvariable=e, font=('Comic Sans MS', 20))
expenses.grid(row=11, column=3)


income_report = CTkTextbox(frame, width=450, height=400, state="disabled", corner_radius=0, font=('Arial', 20))
income_report.grid(row=13, columnspan=2, column=0)

expenses_report = CTkTextbox(frame, width=450, height=400, state="disabled", corner_radius=0, font=('Arial', 20))
expenses_report.grid(row=13, columnspan=2, column=2)


CTkLabel(frame, height=5, text="").grid(row=0, columnspan=4)
CTkLabel(frame, height=5, text="").grid(row=2, columnspan=4)
CTkLabel(frame, height=5, text="").grid(row=4, columnspan=4)
CTkLabel(frame, height=5, text="").grid(row=6, columnspan=4)
CTkLabel(frame, height=30, text="").grid(row=8, columnspan=4)
CTkLabel(frame, height=5, text="").grid(row=10, columnspan=4)
CTkLabel(frame, height=5, text="").grid(row=12, columnspan=4)

window.mainloop()