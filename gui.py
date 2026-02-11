import tkinter as tk
import vault as V
import guiFuncs as GF
import hashlib as HL
import os

def guiMain():

### Set up Window ###
    window = tk.Tk()
    columns = 11
    rows = 7
    screenHeight = window.winfo_screenheight()
    screenWeight = window.winfo_screenwidth()
        
    window.title('Password Manager')
    window.geometry(f'{screenWeight}x{screenHeight}')

    for c in range(columns):
        window.columnconfigure(c, weight=1)
    for r in range(rows):
        window.rowconfigure(r, weight=1)
####################

### Header ###
    welcomeLabel = tk.Label(
        window, 
        text='Password Manager', 
        font=("Arial", 30, 'underline')
        )
    welcomeLabel.grid(
        row=0,
        column=0, 
        columnspan=columns, 
        sticky='n', 
        pady=20)

##############

### Container (body) ###
    container = tk.Frame(window)

    container.grid(row=1, 
                   column=0, 
                   columnspan=columns, 
                   rowspan=rows-1, 
                   sticky='nsew'
                   )
    
    container.rowconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)
########################

    if not os.path.exists('passwords.enc'):
        GF.showCreateAccount(container, rows, columns)
    else:
        GF.showLogin(container, rows, columns)

    window.mainloop()

