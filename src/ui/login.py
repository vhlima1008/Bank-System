import customtkinter as ctk
from theme import PRIMARY_BG, SURFACE_BG, TEXT, ACCENT, BORDER, ALERT_RED_SOFT, darker

ACCENT_HOVER = darker(ACCENT, 0.78)

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master, corner_radius=18, fg_color=SURFACE_BG)
        self.on_login = on_login

        self.font_h1 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        self.font_h2 = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        self.font_h3 = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_md = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_sm = ctk.CTkFont(family="Segoe UI", size=12)

        self.usernameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()

        self._login_error_lbl = None
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=PRIMARY_BG, corner_radius=14)
        header.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="nwe")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header, text="Digital Bank", text_color=TEXT, font=self.font_h1
        ).grid(row=0, column=0, padx=16, pady=12, sticky="w")

        # Form Card
        card = ctk.CTkFrame(
            self, fg_color=SURFACE_BG, corner_radius=16,
            border_color=BORDER, border_width=1
        )
        card.grid(row=1, column=0, padx=24, pady=(8, 16), sticky="nwe")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Acesso ao Digital Bank", text_color=TEXT, font=self.font_h2
                     ).grid(row=0, column=0, padx=20, pady=(20, 6), sticky="w")
        ctk.CTkLabel(card, text="Entre com suas credenciais", text_color=TEXT, font=self.font_sm
                     ).grid(row=1, column=0, padx=20, pady=(0, 12), sticky="w")

        # User
        ctk.CTkLabel(card, text="Usuário", text_color=TEXT, font=self.font_h3
                     ).grid(row=2, column=0, padx=20, pady=(8, 4), sticky="w")
        userEntry = ctk.CTkEntry(
            card, textvariable=self.usernameVar, fg_color=PRIMARY_BG, text_color=TEXT,
            border_color=BORDER, corner_radius=10, height=38, placeholder_text="Seu usuário"
        )
        userEntry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="we")

        # Password
        ctk.CTkLabel(card, text="Senha", text_color=TEXT, font=self.font_h3
                     ).grid(row=4, column=0, padx=20, pady=(8, 4), sticky="w")
        pwd_row = ctk.CTkFrame(card, fg_color="transparent")
        pwd_row.grid(row=5, column=0, padx=20, pady=(0, 16), sticky="we")
        pwd_row.grid_columnconfigure(0, weight=1)
        pwdEntry = ctk.CTkEntry(
            pwd_row, textvariable=self.passwordVar, show="*", fg_color=PRIMARY_BG, text_color=TEXT,
            border_color=BORDER, corner_radius=10, height=38, placeholder_text="Sua senha"
        )
        pwdEntry.grid(row=0, column=0, sticky="we")

        def toggle_pwd():
            if pwdEntry.cget("show") == "*":
                pwdEntry.configure(show="")
                toggle_btn.configure(text="Ocultar")
            else:
                pwdEntry.configure(show="*")
                toggle_btn.configure(text="Mostrar")

        toggle_btn = ctk.CTkButton(
            pwd_row, text="Mostrar", width=90, height=38,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=PRIMARY_BG,
            corner_radius=10, command=toggle_pwd
        )
        toggle_btn.grid(row=0, column=1, padx=(8, 0), sticky="e")

        # Login Button
        loginBtn = ctk.CTkButton(
            card, text="Entrar", command=self.onLoginClicked,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=PRIMARY_BG,
            corner_radius=10, height=42
        )
        loginBtn.grid(row=6, column=0, padx=20, pady=(4, 20), sticky="we")

        # Error message
        self._login_error_lbl = ctk.CTkLabel(
            self.loginFrame, text="", text_color=ALERT_RED_SOFT, font=self.font_sm
        )
        self._login_error_lbl.grid(row=2, column=0, padx=16, pady=(0, 6), sticky="we")
        self._login_error_lbl.grid_remove()

        # Footer
        footer = ctk.CTkLabel(self.loginFrame, text="© 2025 Digital Bank", text_color=TEXT, font=self.font_sm)
        footer.grid(row=7, column=0, padx=16, pady=(4, 8), sticky="e")

        userEntry.focus_set()

        def _try_login(self):
            user = self.usernameVar.get().strip()
            pwd = hash(self.passwordVar.get().strip())

            if user and pwd:
                self._login_error_lbl.grid_remove()
                self.on_login(user)
            else:
                self._login_error_lbl.configure(text="Usuário e senha obrigatórios.")
                self._login_error_lbl.grid()