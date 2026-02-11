import tkinter as tk
import vault as V


def clearContainer(container):
    for widget in container.winfo_children():
        widget.destroy()

def showCreateAccount(parent,rows,columns):
    clearContainer(parent)
    center_col = columns // 2
    center_row = rows // 2

    frame = tk.Frame(parent)
    frame.grid(row=0,column=0, sticky='nsew')
    for column in range(columns):
        frame.columnconfigure(column, weight=1)
    for row in range(rows):
        frame.rowconfigure(row, weight=1)

    tk.Label(frame, text="Create MasterKey to Start!", font=("Arial", 24)).grid(
        row=center_row - 2, 
        column=0, 
        columnspan=columns
        )

    tk.Label(frame, text="Master Key:").grid(
        row=center_row - 1, 
        column=center_col - 1, 
        sticky='e'
        )
    
    tk.Label(frame, text="Confirm Key:").grid(
        row=center_row, 
        column=center_col - 1, 
        sticky='e'
        )


    masterkey_entry = tk.Entry(frame, show="*", width=25)
    masterkey_entry.grid(
        row=center_row - 1, 
        column=center_col, 
        sticky="w"
        )


    confirmkey_entry = tk.Entry(frame, show="*", width=25)
    confirmkey_entry.grid(
        row=center_row, 
        column=center_col, 
        sticky="w"
        )
    
    error_label = tk.Label(frame, text='', font=('Arial', 20), fg="red")
    error_label.grid(
        row=center_row + 1, 
        column = 0, 
        columnspan=columns)

    def create_account():
        key1 = masterkey_entry.get().strip()
        key2 = confirmkey_entry.get().strip()

        if key1 == '' or key2 == '':
            error_label.config(text='Keys cannot be empty!')
            return

        if key1 != key2:
            error_label.config(text="Keys do not match!")
            return
        
        V.saveVault({}, key1)
        error_label.config(text="Vault Created!", fg="blue")

        parent.after(500, lambda: showLogin(parent, rows, columns))
        

    tk.Button(frame, text='Create Account', width=50, height=2, font=('Arial', 20), command=create_account).grid(
        row=center_row + 2, 
        column=0, 
        columnspan=columns
        )

def showLogin(parent, rows, columns):
    clearContainer(parent)
    center_row = rows // 2
    center_col = columns // 2

    frame = tk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    for row in range(rows):
        frame.rowconfigure(row, weight=1)
    for column in range(columns):
        frame.columnconfigure(column, weight=1)
    
    tk.Label(frame, text="Enter MasterKey: ", font=("Arial", 20)).grid(
        row=center_row - 1, 
        column=center_col - 1, 
        sticky = 'e'
        )

    key_entry = tk.Entry(frame, show="*", width=25)
    key_entry.grid(
        row=center_row - 1, 
        column=center_col, 
        sticky="w"
        )

    error_label = tk.Label(frame, text='', font=('Arial', 20), fg="red")
    error_label.grid(
        row=center_row + 2, 
        column = center_col - 1, 
        columnspan=2
        )
    
    def chgKeyWindow(parent):
        window1 = tk.Toplevel(parent)
        window1.title("Change MasterKey")
        window1.geometry("600x400")

        tk.Label(window1, text="Current Masterkey:", font=('Arial', 15)).pack(pady=5)
        currentKey = tk.Entry(window1, show='*')
        currentKey.pack(pady=5)

        tk.Label(window1, text="New Masterkey:", font=('Arial', 15)).pack(pady=5)
        newkey1 = tk.Entry(window1, show='*')
        newkey1.pack(pady=5)

        tk.Label(window1, text="Confirm New Masterkey:", font=('Arial', 15)).pack(pady=5)
        newkey2 = tk.Entry(window1, show='*')
        newkey2.pack(pady=5)

        error_label = tk.Label(window1, text='', font=('Arial', 15), fg="red")
        error_label.pack(pady=5)

        def submit():
            typed_masterkey = currentKey.get().strip()

            test_vault = V.loadVault(typed_masterkey)

            if test_vault is None:
                error_label.config(text='Entered Wrong MasterKey!')
                return

            newMasterKey1 = newkey1.get().strip()
            newMasterKey2 = newkey2.get().strip()
            
            if newMasterKey1 != newMasterKey2:
                error_label.config(text="MasterKey's Do Not Match!")
                return
                
            if newMasterKey1 == '':
                error_label.config(text='Please Enter New MasterKey')
                return


            error_label.config(text='MasterKey Changed!', fg='blue')
            V.saveVault(test_vault, newMasterKey1)
            window1.after(500, window1.destroy)



        chgButton = tk.Button(window1, text='Change MasterKey', font=('Arial', 15), command=submit)
        chgButton.pack(pady=5)

    change_MasterKey = tk.Button(frame, text='Change Master Key', font=('Arial', 20), width=25, command=lambda: chgKeyWindow(parent))
    change_MasterKey.grid(
        row=center_row, 
        column=center_col -2, 
        columnspan=4
        ) 

    def submit():
        masterkey = key_entry.get().strip()
        vault1 = V.loadVault(masterkey)

        if vault1 is None:
            error_label.config(text='Incorrect MasterKey!')
        else:
            error_label.config(text='Vault Loaded!', fg='blue')
            from guiFuncs import showAccounts
            parent.after(500, lambda: showAccounts(parent, vault1, masterkey, rows, columns))


    tk.Button(frame, text="Login", font=('Arial', 20), width=25, command=submit).grid(
        row=center_row + 1, 
        column=center_col - 2, 
        columnspan=4
        )

def showAccounts(parent, vault, masterkey, rows, columns):
    clearContainer(parent)

    frame = tk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")

    for row in range(rows):
        frame.rowconfigure(row, weight=1)
    for column in range(columns):
        frame.columnconfigure(column, weight=1)

    frame.rowconfigure(1, weight=5)

    center_col = columns // 2

    tk.Label(frame, text='Accounts', font=('Arial', 20)).grid(
        row = 0,
        column = center_col,
        sticky='n'
    )

    listbox_frame = tk.Frame(frame)
    listbox_frame.grid(row=1, column=center_col, sticky="nsew")

    listbox_frame.rowconfigure(0, weight=1)
    listbox_frame.columnconfigure(0, weight=1)

    accountBox = tk.Listbox(listbox_frame, font=('Arial', 14))
    accountBox.grid(
        row = 0,
        column = 0,
        sticky='nsew'
    )

    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=accountBox.yview)
    scrollbar.grid(
        row = 0,
        column= 1,
        sticky='ns'
    )

    accountBox.config(yscrollcommand=scrollbar.set)

    for account in vault:
        accountBox.insert(tk.END, account.capitalize())

    details_frame = tk.Frame(frame)
    details_frame.grid(row=1, column=center_col + 2, sticky="n")

    current_password = {'value': ""}

    tk.Label(details_frame, text="Username:", font=('Arial', 15)).pack()
    username_label = tk.Label(details_frame, text="")
    username_label.pack(pady=5)

    tk.Label(details_frame, text="Password:", font=('Arial', 15)).pack()
    password_label = tk.Label(details_frame, text="")
    password_label.pack(pady=5)

    toggle_btn = tk.Button(details_frame, text="Show")
    toggle_btn.pack(pady=5)

    def togglePassword():
        if password_label.cget("text") == "********":
            password_label.config(text=current_password["value"])
            toggle_btn.config(text='Hide')
        else:
            password_label.config(text='********')
            toggle_btn.config(text='Show')

    toggle_btn.config(command=togglePassword)

    def chgInfoWindow(parent, vault, masterkey):
        window1 = tk.Toplevel(parent)
        window1.title("Change Information")
        window1.geometry("600x400")

        tk.Label(window1, text="Change Username:", font=('Arial', 15)).pack(pady=5)
        newuser = tk.Entry(window1)
        newuser.pack(pady=5)

        tk.Label(window1, text="New Password:", font=('Arial', 15)).pack(pady=5)
        newpass1_entry = tk.Entry(window1, show='*')
        newpass1_entry.pack(pady=5)

        tk.Label(window1, text="Confirm Password:", font=('Arial', 15)).pack(pady=5)
        newPass2_entry = tk.Entry(window1, show='*')
        newPass2_entry.pack(pady=5)

        error_label = tk.Label(window1, text='',font=('Arial', 20), fg="red")
        error_label.pack(pady=5)

        def submit():
            selection = accountBox.curselection()
            if not selection:
                error_label.config(text='No account selected')
                return
            
            selected = accountBox.get(selection[0])
            account = selected.lower()

            newUsername = newuser.get().strip()
            pass1 = newpass1_entry.get().strip()
            pass2 = newPass2_entry.get().strip()

            if pass1 != pass2: # passwords aren't the same+
                error_label.config(text="Passwords Do Not Match")
                return

            if newUsername != '' and pass1 != '': # both username and password changed
                vault[account]['password'] = pass1
                vault[account]['username'] = newUsername

                error_label.config(text="Username and Password Changed", fg="blue")

                username_label.config(text=newUsername)
                current_password['value'] = pass1
                password_label.config(text='********')
                toggle_btn.config(text='Show')

                V.saveVault(vault, masterkey)
                window1.after(500, window1.destroy)
                return

            elif newUsername == '' and pass1 != '': # only password changed
                vault[account]['password'] = pass1

                error_label.config(text="Password Changed", fg="blue")

                current_password['value'] = pass1
                password_label.config(text='********')
                toggle_btn.config(text='Show')

                V.saveVault(vault, masterkey)
                window1.after(500, window1.destroy)
                return

            elif newUsername != '' and pass1 == '': # only username changed
                vault[account]['username'] = newUsername

                error_label.config(text="Username Changed", fg="blue")
                username_label.config(text=newUsername)
                V.saveVault(vault, masterkey)
                window1.after(500, window1.destroy)
                return

            else: # nothing changed
                error_label.config(text="No Information Provided")

        tk.Button(window1, text='Change', font=('Arial', 15), command=submit).pack(pady=5)

    tk.Button(details_frame, text='Change Info', font=('Arial', 15), command=lambda: chgInfoWindow(parent, vault, masterkey)).pack()


    def showDetails(event):
        selection = accountBox.curselection()
        if not selection:
            return

        selected = accountBox.get(selection[0])
        account = selected.lower()

        data = vault[account]

        current_password['value'] = data['password']
        password_label.config(text='********')
        toggle_btn.config(text='Show')

        username_label.config(text=data["username"])
   
    accountBox.bind("<<ListboxSelect>>", showDetails)
    

    def AddAccountWindow(parent, vault, masterkey, accountBox):
        addAccWindow = tk.Toplevel(parent)
        addAccWindow.title("Add Account")
        addAccWindow.geometry("600x400")

        tk.Label(addAccWindow, text="Application Name:").pack(pady=5)
        application_entry = tk.Entry(addAccWindow)
        application_entry.pack(pady=5)

        tk.Label(addAccWindow, text="Username:").pack(pady=5)
        username_entry = tk.Entry(addAccWindow)
        username_entry.pack(pady=5)

        tk.Label(addAccWindow, text="Password:").pack(pady=5)
        password_entry = tk.Entry(addAccWindow, show="*")
        password_entry.pack(pady=5)
        
        error_label_add = tk.Label(addAccWindow, text='', fg='red')
        error_label_add.pack(pady=5)

        def submit():
            appName = application_entry.get().strip().lower()

            if appName == '':
                error_label_add.config(text='No Account Entered!')
                return

            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if password == '':
                error_label_add.config(text='Password Required')
                return
            
            if appName in vault:
                error_label_add.config(text='Account already exists!')
                return
            
            error_label_add.config(text='Account Added!', fg='blue')

            vault[appName] = {'username': username, 'password': password}

            accountBox.insert(tk.END, appName.capitalize())
            V.saveVault(vault, masterkey)
            addAccWindow.destroy()

        tk.Button(addAccWindow, text="Save", command=submit).pack(pady=10)

    def DelAccountWindow(parent, vault, masterkey, accountBox):
        delAccWindow = tk.Toplevel(parent)
        delAccWindow.title("Delete Account")
        delAccWindow.geometry("600x400")

        tk.Label(delAccWindow, text="Application Name:").pack(pady=5)
        application_entry = tk.Entry(delAccWindow)
        application_entry.pack(pady=5)

        error_label_del = tk.Label(delAccWindow, text="", fg='red')
        error_label_del.pack(pady=5)


        def submit():
            appName = application_entry.get().strip().lower()
            appName_capitalize = appName.capitalize()

            if appName not in vault:
                error_label_del.config(text='Account Not Found!')
                return
            
            error_label_del.config(text='Account Deleted!', fg='blue')

            del vault[appName]

            items= accountBox.get(0, tk.END)

            if appName_capitalize in items:
                index = items.index(appName_capitalize)
                accountBox.delete(index)
            V.saveVault(vault, masterkey)
            delAccWindow.destroy()
        tk.Button(delAccWindow, text="Delete", command=submit).pack(pady=10)

    def FilterAccountsWindow(parent, vault, accountBox):
        filAccWindow = tk.Toplevel(parent)
        filAccWindow.title("Filter Accounts")
        filAccWindow.geometry("600x400")

        tk.Button(filAccWindow, text='A --> Z', command=lambda: refreshAccountList(accountBox, vault, False)).pack(pady=10)

        tk.Button(filAccWindow, text='Z --> A', command=lambda: refreshAccountList(accountBox, vault, True)).pack(pady=10)

        tk.Label(filAccWindow, text='Search:').pack(pady=5)
        search_entry = tk.Entry(filAccWindow)
        search_entry.pack(pady=5)

        def update(*args):
            filterAccounts(accountBox, vault, search_entry.get())  

        search_entry.bind("<KeyRelease>", update)      

    tk.Button(frame, text='Add Account', font=('Arial', 15), command=lambda: AddAccountWindow(parent, vault, masterkey, accountBox)).grid(
        row = 1,
        column=center_col - 1,
        sticky='n',
        pady=(50,0)
    )
   
    tk.Button(frame, text='Delete Account', font=('Arial', 15), command=lambda: DelAccountWindow(parent, vault, masterkey, accountBox)).grid(
        row = 1,
        column= center_col - 1,
        sticky='s',
        pady=(0,50)
    )

    tk.Button(frame, text='Filter Accounts', font=('Arial', 15), command=lambda: FilterAccountsWindow(parent, vault, accountBox)).grid(
        row = 1,
        column= center_col - 1,
    )

def refreshAccountList(accountBox, vault, reverse=False):
    accountBox.delete(0, tk.END)    

    accounts = sorted(vault.keys(), reverse=reverse)

    for account in accounts:
        accountBox.insert(tk.END, account.capitalize())

def filterAccounts(accountBox, vault, search_text):
    accountBox.delete(0, tk.END)

    search_text = search_text.strip().lower()

    for account in vault:
        if account.lower().startswith(search_text):
            accountBox.insert(tk.END, account.capitalize())

