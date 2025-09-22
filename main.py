import customtkinter as ctk

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup ---------------------------------------------------------
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.title('Digital Bank')
        self.geometry('720x480')

        # Entry Variables ------------------------------------------------------
        self.usernameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()
        self.accountVar = 0.0
        

        # Component Creation ---------------------------------------------------
        self.createDashboardFrame()

    # Login Screen -------------------------------------------------------------
    def createLoginFrame(self):
        self.loginFrame = ctk.CTkFrame(self, corner_radius=16)
        self.loginFrame.place(relx=0.75, rely=0.5, anchor='center', relwidth=0.38, relheight=0.82)
        self.loginFrame.lift()

        self.loginFrame.grid_rowconfigure((0,1,2,3,4,5), weight=0)
        self.loginFrame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self.loginFrame, text='Acess to Digital Bank', font=('Segoe UI', 20, 'bold'))
        title.grid(row=0, column=0, padx=24, pady=(24, 12), sticky='nwe')

        userLabel = ctk.CTkLabel(self.loginFrame, text='Username', font=('Segoe UI', 15, 'bold'))
        userLabel.grid(row=1, column=0, padx=24, pady=(8, 4), sticky='w')
        userEntry = ctk.CTkEntry(self.loginFrame, textvariable=self.usernameVar)
        userEntry.grid(row=2, column=0, padx=24, pady=(8, 4), sticky='we')

        passwordLabel = ctk.CTkLabel(self.loginFrame, text='Password', font=('Segoe UI', 15, 'bold'))
        passwordLabel.grid(row=3, column=0, padx=24, pady=(8, 4), sticky='w')
        passwordEntry = ctk.CTkEntry(self.loginFrame, textvariable=self.passwordVar, show='*')
        passwordEntry.grid(row=4, column=0, padx=24, pady=(8, 4), sticky='we')

        loginButton = ctk.CTkButton(self.loginFrame, text='Login', command=self.onLoginClicked)
        loginButton.grid(row=6, column=0, padx=24, pady=(8, 24), sticky='we')
    
    # Dashboard Screen ---------------------------------------------------------
    def createDashboardFrame(self):
        self.dashboardFrame = ctk.CTkFrame(self, corner_radius=16)
        self.dashboardFrame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.75, relheight=0.82)
        self.dashboardFrame.lift()

        self.dashboardFrame.grid_rowconfigure((0,1,2,3,4,5), weight=0)
        self.dashboardFrame.grid_columnconfigure((0,1,2,3,4,5), weight=0)

        # Elements in dashboardFrame -------------------------------------------
        entranceLabel = ctk.CTkLabel(self.dashboardFrame, text=f'Hello, {self.usernameVar.get()}', font=('Segoe UI', 20, 'bold'))
        entranceLabel.grid(row=0, column=0, padx=24, pady=(24, 12), sticky='nwe')

        accountLabel = ctk.CTkLabel(self.dashboardFrame, text=f'${self.accountVar}', font=('Segoe UI', 20, 'bold'))
        accountLabel.grid(row=0, column=1, padx=24, pady=(24, 12), sticky='nwe')

        actionFrame = ctk.CTkFrame(self.dashboardFrame, corner_radius=16)
        actionFrame.grid(row=1, rowspan=5, column=0, padx=24, pady=24, sticky='nwe')
        actionFrame.lift()

        actionFrame.grid_rowconfigure((0,1,2,3,4,5), weight=0)
        actionFrame.grid_columnconfigure(0, weight=1)

        self.depositFrame = ctk.CTkFrame(self.dashboardFrame, corner_radius=16)
        self.depositFrame.grid(row=1, rowspan=5, column=1, columnspan=5, padx=24, pady=24, sticky='nwe')
        self.depositFrame.lift()

        # Elements in actionFrame ----------------------------------------------
        depositButton = ctk.CTkButton(actionFrame, text="Deposit")
        depositButton.grid(row=1, column=0, padx=12, pady=(12, 6), sticky='nwe')

        withdrawButton = ctk.CTkButton(actionFrame, text="Withdraw")
        withdrawButton.grid(row=2, column=0, padx=12, pady=(12, 6), sticky='nwe')

        extractButton = ctk.CTkButton(actionFrame, text="Extract")
        extractButton.grid(row=3, column=0, padx=12, pady=(12, 6), sticky='nwe')

        financingButton = ctk.CTkButton(actionFrame, text="Financing")
        financingButton.grid(row=4, column=0, padx=12, pady=(12, 6), sticky='nwe')

        logoutButton = ctk.CTkButton(actionFrame, text="Logout", command=self.onLogoutClicked)
        logoutButton.grid(row=6, column=0, padx=12, pady=(12, 6), sticky='nwe')



    
    # Methods ------------------------------------------------------------------
    def onLoginClicked(self):
        user = self.usernameVar.get().strip()
        pwd = hash(self.passwordVar.get())
        if user and pwd:
            print('Logged-in')
            self.loginFrame.destroy()
            self.createDashboardFrame()
        else:
            print('Wrong way!')
    
    def onLogoutClicked(self):
        self.dashboardFrame.destroy()
        self.createLoginFrame()


if __name__ == '__main__':
    app = LoginApp()
    app.mainloop()