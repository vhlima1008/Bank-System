import customtkinter as ctk

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Login System")
        self.geometry("500x350")

        # Entry Var
        self.usernameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()
        self.depositVar = ctk.DoubleVar(value=0.0)
        self.account = 0
        self.extract = []

        # Component Creation
        self.loginFrame = None
        self.mainFrame = None
        self.depositFrame = None
        self.createLoginFrame()

    # Login Screen -------------------------------------------------------------
    def createLoginFrame(self):
        self.loginFrame = ctk.CTkFrame(master=self)
        self.loginFrame.pack(pady=20, padx=60, fill="both", expand=True)

        loginLabel = ctk.CTkLabel(master=self.loginFrame, text="Login System")
        loginLabel.pack(pady=12, padx=10)

        # User Input
        usernameEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Username",
            textvariable=self.usernameVar
        )
        usernameEntry.pack(pady=12, padx=10)

        # Password Input
        passwordEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Password",
            show="*",
            textvariable=self.passwordVar
        )
        passwordEntry.pack(pady=12, padx=10)

        # login Button
        loginButton = ctk.CTkButton(
            master=self.loginFrame,
            text="Login",
            command=self.login
        )
        loginButton.pack(pady=12, padx=10)

        # Checkbox
        loginCheckbox = ctk.CTkCheckBox(master=self.loginFrame, text="Remember Me")
        loginCheckbox.pack(pady=12, padx=10)

    # Main Screen -------------------------------------------------------------
    def createMainFrame(self, username):
        self.mainFrame = ctk.CTkFrame(master=self)
        self.mainFrame.pack(pady=20, padx=60, fill="both", expand=True)

        mainLabel = ctk.CTkLabel(master=self.mainFrame, text=f"{username}' Account.")
        mainLabel.pack(pady=12, padx=10)

        accountLabel = ctk.CTkLabel(
            master=self.mainFrame,
            text=f"Account: {self.account}",
            font=("Arial", 20)
        )
        accountLabel.pack(pady=20)

        depositButton = ctk.CTkButton(
            master=self.mainFrame,
            text="Deposit a value",
            command=self.openDepositScreen
        )
        depositButton.pack(pady=10)


        logoutButton = ctk.CTkButton(
            master=self.mainFrame,
            text="Logout",
            command=self.logout
        )
        logoutButton.pack(pady=10)
    
    # Deposit Screen -------------------------------------------------------------
    def createDepositFrame(self):
        self.depositFrame = ctk.CTkFrame(master=self)
        self.depositFrame.pack(pady=20, padx=60, fill="both", expand=True)

        depositLabel = ctk.CTkLabel(master=self.depositFrame, text="Deposit")
        depositLabel.pack(pady=12, padx=10)

        # Deposit Input
        depositEntry = ctk.CTkEntry(
            master=self.depositFrame,
            placeholder_text="$100,00",
            textvariable=self.depositVar
        )
        depositEntry.pack(pady=12, padx=10)

        # Confirm Button
        confirmButton = ctk.CTkButton(
            master=self.depositFrame,
            text="Deposit it",
            command=self.depositValue
        )
        confirmButton.pack(pady=12, padx=10)

        # Close Button
        closeButton = ctk.CTkButton(
            master=self.depositFrame,
            text="Close",
            command=self.closeDepositScreen
        )
        closeButton.pack(pady=12, padx=10)

    # Methods ------------------------------------------------------------------
    def login(self):
        passwordHashed = hash(self.passwordVar.get())
        username = self.usernameVar.get()

        print("Username:", username)
        print("Password Hash:", passwordHashed)

        if self.loginFrame is not None:
            self.loginFrame.destroy()

        self.createMainFrame(username)
    

    def logout(self):
        if self.mainFrame is not None:
            self.mainFrame.destroy()

        self.usernameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()

        self.createLoginFrame()

    def openDepositScreen(self):
        if self.mainFrame is not None:
            self.mainFrame.destroy()

        self.createDepositFrame()

    def closeDepositScreen(self):
        if self.depositFrame is not None:
            self.depositFrame.destroy()
        username = self.usernameVar.get()
        
        self.createMainFrame(username)

    def depositValue(self):
        value = float(self.depositVar.get() or 0)  # get the value
        self.account += value
        self.extract.append(f"Deposited: {value}")

        # after deposited, come to main
        if self.depositFrame is not None:
            self.depositFrame.destroy()
        self.createMainFrame(self.usernameVar.get())


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()