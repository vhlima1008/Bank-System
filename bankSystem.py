import customtkinter as ctk

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Digital Bank")
        self.geometry("480x720")

        # >>> raiz com grid para permitir centralização
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

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

    # ---------------- Login Screen ----------------
    def createLoginFrame(self):
        self.loginFrame = ctk.CTkFrame(self)
        # >>> ocupa a célula 0,0 e expande
        self.loginFrame.grid(row=0, column=0, sticky="nsew")

        # >>> wrapper centralizado
        content = ctk.CTkFrame(self.loginFrame)
        content.pack(expand=True)  # <- centra vertical e horizontalmente

        loginLabel = ctk.CTkLabel(content, text="Login System")
        loginLabel.pack(pady=12, padx=10)

        usernameLabel = ctk.CTkLabel(content, text="Username", font=("Arial", 12))
        usernameLabel.pack(pady=(0, 0), padx=10)

        usernameEntry = ctk.CTkEntry(content, placeholder_text="Username",
                                     textvariable=self.usernameVar)
        usernameEntry.pack(pady=12, padx=10)

        passwordLabel = ctk.CTkLabel(content, text="Password", font=("Arial", 12))
        passwordLabel.pack(pady=(0, 0), padx=10)

        passwordEntry = ctk.CTkEntry(content, placeholder_text="Password",
                                     show="*", textvariable=self.passwordVar)
        passwordEntry.pack(pady=12, padx=10)

        loginButton = ctk.CTkButton(content, text="Login", command=self.login)
        loginButton.pack(pady=12, padx=10)

    # ---------------- Main Screen ----------------
    def createMainFrame(self, username):
        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        content = ctk.CTkFrame(self.mainFrame)
        content.pack(expand=True)

        mainLabel = ctk.CTkLabel(content, text=f"{username}' Account.")
        mainLabel.pack(pady=12, padx=10)

        accountLabel = ctk.CTkLabel(content, text=f"Account: {self.account}", font=("Arial", 20))
        accountLabel.pack(pady=20)

        depositButton = ctk.CTkButton(content, text="Deposit a value",
                                      command=self.openDepositScreen)
        depositButton.pack(pady=10)

        logoutButton = ctk.CTkButton(content, text="Logout", command=self.logout)
        logoutButton.pack(pady=10)

    # --------------- Deposit Screen ---------------
    def createDepositFrame(self):
        self.depositFrame = ctk.CTkFrame(self)
        self.depositFrame.grid(row=0, column=0, sticky="nsew")

        content = ctk.CTkFrame(self.depositFrame)
        content.pack(expand=True)

        depositLabel = ctk.CTkLabel(content, text="Deposit")
        depositLabel.pack(pady=12, padx=10)

        depositEntry = ctk.CTkEntry(content, placeholder_text="$100,00",
                                    textvariable=self.depositVar)
        depositEntry.pack(pady=12, padx=10)

        confirmButton = ctk.CTkButton(content, text="Deposit it",
                                      command=self.depositValue)
        confirmButton.pack(pady=12, padx=10)

        closeButton = ctk.CTkButton(content, text="Close",
                                    command=self.closeDepositScreen)
        closeButton.pack(pady=12, padx=10)

    # ---------------- Methods ----------------
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
        self.usernameVar.set("")
        self.passwordVar.set("")
        self.createLoginFrame()

    def openDepositScreen(self):
        if self.mainFrame is not None:
            self.mainFrame.destroy()
        self.createDepositFrame()

    def closeDepositScreen(self):
        if self.depositFrame is not None:
            self.depositFrame.destroy()
        self.createMainFrame(self.usernameVar.get())

    def depositValue(self):
        value = float(self.depositVar.get() or 0)
        self.account += value
        self.extract.append(f"Deposited: {value}")
        if self.depositFrame is not None:
            self.depositFrame.destroy()
        self.createMainFrame(self.usernameVar.get())


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
