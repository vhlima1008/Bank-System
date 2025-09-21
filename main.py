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
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()

        # Component Creation
        self.create_widgets()

    def create_widgets(self):
        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(master=frame, text="Login System")
        label.pack(pady=12, padx=10)

        # User Input
        name_entry = ctk.CTkEntry(
            master=frame,
            placeholder_text="Username",
            textvariable=self.username_var
        )
        name_entry.pack(pady=12, padx=10)

        # Password Input
        password_entry = ctk.CTkEntry(
            master=frame,
            placeholder_text="Password",
            show="*",
            textvariable=self.password_var
        )
        password_entry.pack(pady=12, padx=10)

        # login Button
        login_button = ctk.CTkButton(
            master=frame,
            text="Login",
            command=self.login
        )
        login_button.pack(pady=12, padx=10)

        # Checkbox
        checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
        checkbox.pack(pady=12, padx=10)

    def login(self):
        password_hashed = hash(self.password_var.get())
        print("Username:", self.username_var.get())
        print("Password Hash:", password_hashed)


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
