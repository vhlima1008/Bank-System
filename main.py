import customtkinter as ctk
from datetime import datetime

DATE_FMT = "%Y-%m-%d %H:%M:%S"

# ---------------------- Theme/Colors ----------------------
PRIMARY_BG = "#353941"   # Main Background
SURFACE_BG = "#26282B"   # Cards/Frames
ACCENT     = "#5F85DB"   # Buttons
TEXT       = "#D1E3FF"   # Texts
BORDER     = "#26282B"   # Borders

# Alert colors 
ALERT_RED       = "#EF4444"  # Main Red
ALERT_RED_SOFT  = "#FCA5A5"  # Text Red
ALERT_RED_DARK  = "#7F1D1D"  # Background Red

def darker(hex_color: str, factor: float = 0.85) -> str:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return f"#{r:02x}{g:02x}{b:02x}"

ACCENT_HOVER = darker(ACCENT, 0.78)

# ---------------------- App ----------------------
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window/Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Digital Bank")
        self.geometry("880x560")  # window size when start
        self.minsize(800, 560)
        self.configure(fg_color=PRIMARY_BG)

        # Variables
        self.usernameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()
        self.accountVar  = 0.0
        self.extractVar = []
        self.dateTimeVar = datetime.now().strftime(DATE_FMT)

        # References for Hide/Show
        self._login_error_lbl = None
        self._sidebar = None
        self._content = None
        self.loginFrame = None
        self.dashboardFrame = None

        # Adjusted Fonts
        self.font_h1 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        self.font_h2 = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        self.font_h3 = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_md = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_sm = ctk.CTkFont(family="Segoe UI", size=12)

        # Base Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Screen Container
        self.screenContainer = ctk.CTkFrame(self, fg_color=PRIMARY_BG)
        self.screenContainer.grid(row=0, column=0, sticky="nsew")
        self.screenContainer.grid_rowconfigure(0, weight=1)
        self.screenContainer.grid_columnconfigure(0, weight=1)

        # Main Frame
        self.createLoginFrame()

        # Shortcuts
        self.bind("<Return>", lambda e: self.onLoginClicked())   # Enter no login
        self.bind("<Escape>", lambda e: self.onLogoutClicked())  # Esc para voltar do dashboard

        # Reponsibility
        self.bind("<Configure>", self._on_resize)

    # ---------------------- Login ----------------------
    def createLoginFrame(self):
        if self.dashboardFrame:
            self.dashboardFrame.grid_forget()

        self.loginFrame = ctk.CTkFrame(self.screenContainer, corner_radius=18, fg_color=SURFACE_BG)
        self.loginFrame.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")

        # Internal Grade
        self.loginFrame.grid_columnconfigure(0, weight=1)
        for r in range(0, 9):
            self.loginFrame.grid_rowconfigure(r, weight=0)
        self.loginFrame.grid_rowconfigure(8, weight=1)

        # Header
        header = ctk.CTkFrame(self.loginFrame, fg_color=PRIMARY_BG, corner_radius=14)
        header.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="nwe")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header, text="Digital Bank", text_color=TEXT, font=self.font_h1
        ).grid(row=0, column=0, padx=16, pady=12, sticky="w")

        # Form Card
        card = ctk.CTkFrame(
            self.loginFrame, fg_color=SURFACE_BG, corner_radius=16,
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

    # ---------------------- Dashboard ----------------------
    def createDashboardFrame(self):
        if self.loginFrame:
            self.loginFrame.grid_forget()

        self.dashboardFrame = ctk.CTkFrame(self.screenContainer, corner_radius=18, fg_color=SURFACE_BG)
        self.dashboardFrame.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")

        # Base Grid for Dashboard
        self.dashboardFrame.grid_rowconfigure(0, weight=0)   # header
        self.dashboardFrame.grid_rowconfigure(1, weight=1)   # body
        self.dashboardFrame.grid_columnconfigure(0, weight=0, minsize=260)  # sidebar
        self.dashboardFrame.grid_columnconfigure(1, weight=1)               # content

        # Header
        header = ctk.CTkFrame(self.dashboardFrame, fg_color=PRIMARY_BG, corner_radius=14)
        header.grid(row=0, column=0, columnspan=2, padx=16, pady=(16, 8), sticky="nwe")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(
            header, text=f"Olá, {self.usernameVar.get() or 'Cliente'}", text_color=TEXT, font=self.font_h2
        ).grid(row=0, column=0, padx=16, pady=12, sticky="w")

        logoutBtn = ctk.CTkButton(
            header, text="Sair", command=self.onLogoutClicked,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=PRIMARY_BG,
            corner_radius=10, height=34, width=100
        )
        logoutBtn.grid(row=0, column=1, padx=16, pady=12, sticky="e")

        # Sidebar
        sidebar = ctk.CTkFrame(self.dashboardFrame, fg_color=SURFACE_BG, corner_radius=16, border_color=BORDER, border_width=1)
        sidebar.grid(row=1, column=0, padx=(16, 8), pady=(8, 16), sticky="nsew")
        sidebar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(sidebar, text="Ações", text_color=TEXT, font=self.font_h3
                     ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        def mk_btn(row, text, cmd=None):
            btn = ctk.CTkButton(
                sidebar, text=text, command=cmd or (lambda: None),
                fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=PRIMARY_BG,
                corner_radius=10, height=38
            )
            btn.grid(row=row, column=0, padx=16, pady=(6, 6), sticky="we")
            return btn

        mk_btn(1, "Depósito", self.showDeposit)
        mk_btn(2, "Saque", self.showWithdraw)
        mk_btn(3, "Extrato", self.showExtract)
        mk_btn(4, "Financiamento", self.showFinancing)

        # Content
        content = ctk.CTkFrame(self.dashboardFrame, fg_color=SURFACE_BG, corner_radius=16, border_color=BORDER, border_width=1)
        content.grid(row=1, column=1, padx=(8, 16), pady=(8, 16), sticky="nsew")
        content.grid_rowconfigure(0, weight=0)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Balance Card
        balanceCard = ctk.CTkFrame(content, fg_color=PRIMARY_BG, corner_radius=14)
        balanceCard.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="nwe")
        balanceCard.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(balanceCard, text="Saldo", text_color=TEXT, font=self.font_h3
                     ).grid(row=0, column=0, padx=16, pady=(12, 0), sticky="w")
        self.balanceLbl = ctk.CTkLabel(balanceCard, text=f"R$ {self.accountVar:,.2f}", text_color=ACCENT, font=ctk.CTkFont("Segoe UI", 22, "bold"))
        self.balanceLbl.grid(row=1, column=0, padx=16, pady=(0, 12), sticky="w")

        # Dynamic Area
        self.dynamicArea = ctk.CTkFrame(content, fg_color=SURFACE_BG, corner_radius=14)
        self.dynamicArea.grid(row=1, column=0, padx=16, pady=(8, 16), sticky="nsew")
        self.dynamicArea.grid_columnconfigure(0, weight=1)
        self.dynamicArea.grid_rowconfigure(0, weight=1)

        self._render_welcome()

        # Responsive References
        self._sidebar = sidebar
        self._content = content

    # ---------------------- Dynamic Content ----------------------
    def _clear_dynamic(self):
        for w in self.dynamicArea.winfo_children():
            w.destroy()

    def _render_welcome(self):
        self._clear_dynamic()
        box = ctk.CTkFrame(self.dynamicArea, fg_color=PRIMARY_BG, corner_radius=14)
        box.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        box.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(box, text="Bem-vindo ao seu painel!", text_color=TEXT, font=self.font_h3
                     ).grid(row=0, column=0, padx=16, pady=(16, 6), sticky="w")
        ctk.CTkLabel(box, text="Escolha uma ação na barra lateral para começar.", text_color=TEXT, font=self.font_sm
                     ).grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

    def showDeposit(self):
        self._clear_dynamic()
        card = ctk.CTkFrame(self.dynamicArea, fg_color=PRIMARY_BG, corner_radius=14)
        card.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Depósito", text_color=TEXT, font=self.font_h3
                     ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")
        amount = ctk.CTkEntry(
            card, placeholder_text="Valor (ex.: 100.00)", fg_color=SURFACE_BG, text_color=TEXT,
            border_color=BORDER, corner_radius=10, height=38
        )
        amount.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="we")

        def do_deposit():
            try:
                val = float(amount.get())
                if val <= 0:
                    raise ValueError
                self.accountVar += val
                self.extractVar.append(f'{self.dateTimeVar} | Depósito R${val} | Saldo R${self.accountVar}')
                print(self.extractVar)
                self.balanceLbl.configure(text=f"R$ {self.accountVar:,.2f}")
                self._render_feedback("Depósito realizado com sucesso.")
            except Exception:
                self._render_feedback("Valor inválido para depósito.", error=True)

        ctk.CTkButton(card, text="Confirmar", command=do_deposit,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=PRIMARY_BG,
                      corner_radius=10, height=40
                      ).grid(row=2, column=0, padx=16, pady=(6, 16), sticky="we")

    def showWithdraw(self):
        self._clear_dynamic()
        card = ctk.CTkFrame(self.dynamicArea, fg_color=PRIMARY_BG, corner_radius=14)
        card.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Saque", text_color=TEXT, font=self.font_h3
                     ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")
        amount = ctk.CTkEntry(
            card, placeholder_text="Valor (ex.: 50.00)", fg_color=SURFACE_BG, text_color=TEXT,
            border_color=BORDER, corner_radius=10, height=38
        )
        amount.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="we")

        def do_withdraw():
            try:
                val = float(amount.get())
                if val <= 0 or val > self.accountVar:
                    raise ValueError
                self.accountVar -= val
                self.extractVar.append(f'{self.dateTimeVar} | Saque R${val} | Saldo R${self.accountVar}')
                print(self.extractVar)
                self.balanceLbl.configure(text=f"R$ {self.accountVar:,.2f}")
                self._render_feedback("Saque realizado com sucesso.")
            except Exception:
                self._render_feedback("Valor inválido ou saldo insuficiente.", error=True)

        ctk.CTkButton(card, text="Confirmar", command=do_withdraw,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=PRIMARY_BG,
                      corner_radius=10, height=40
                      ).grid(row=2, column=0, padx=16, pady=(6, 16), sticky="we")

    def showExtract(self):
        self._clear_dynamic()
        card = ctk.CTkFrame(self.dynamicArea, fg_color=PRIMARY_BG, corner_radius=14)
        card.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Extrato", text_color=TEXT, font=self.font_h3
                     ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")
        
        if len(self.extractVar) != 0:
            box = ctk.CTkTextbox(card, width=300, height=200, text_color=TEXT, font=self.font_md, fg_color=SURFACE_BG)
            box.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")

            for i in self.extractVar:
                box.insert("end", f"{i}\n")
        else:
            ctk.CTkLabel(card, text="Nenhum movimento.", text_color=TEXT, font=self.font_md, fg_color=SURFACE_BG
                           ).grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")

    def showFinancing(self):
        self._clear_dynamic()
        card = ctk.CTkFrame(self.dynamicArea, fg_color=PRIMARY_BG, corner_radius=14)
        card.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Financiamento (demo)", text_color=TEXT, font=self.font_h3
                     ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")
        ctk.CTkLabel(card, text="Simuladores e propostas entrarão aqui.",
                     text_color=TEXT, font=self.font_sm
                     ).grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

    def _render_feedback(self, message: str, error: bool = False):
        color_bg = ALERT_RED_DARK if error else PRIMARY_BG
        color_text = ALERT_RED_SOFT if error else ACCENT
        bar = ctk.CTkFrame(self.dynamicArea, fg_color=color_bg, corner_radius=10)
        bar.grid(row=2, column=0, padx=8, pady=(0, 8), sticky="we")
        ctk.CTkLabel(bar, text=message, text_color=color_text, font=self.font_md
                     ).pack(padx=12, pady=8)

    # ---------------------- Events ----------------------
    def onLoginClicked(self):
        user = self.usernameVar.get().strip()
        pwd  = hash(self.passwordVar.get().strip())
        # Clean Old Messages
        if self._login_error_lbl:
            self._login_error_lbl.configure(text="")
            self._login_error_lbl.grid_remove()

        if user and pwd:
            self.createDashboardFrame()
            print(user, pwd)
        else:
            # Unique Error Message
            self._login_error_lbl.configure(text="Usuário e senha obrigatórios.", text_color=ALERT_RED_SOFT)
            self._login_error_lbl.grid()

    def onLogoutClicked(self):
        # Comeback to Login
        self.createLoginFrame()

    # ---------------------- Responsividade ----------------------
    def _apply_typography_for_width(self, width: int):
        if width < 480:  # mobile
            self.font_h1.configure(size=18)
            self.font_h2.configure(size=16)
            self.font_h3.configure(size=14)
            self.font_md.configure(size=13)
            self.font_sm.configure(size=11)
        elif width < 1200:  # tablet
            self.font_h1.configure(size=20)
            self.font_h2.configure(size=18)
            self.font_h3.configure(size=16)
            self.font_md.configure(size=14)
            self.font_sm.configure(size=12)
        else:  # desktop
            self.font_h1.configure(size=22)
            self.font_h2.configure(size=20)
            self.font_h3.configure(size=18)
            self.font_md.configure(size=15)
            self.font_sm.configure(size=13)

    def _on_resize(self, event):
        width = self.winfo_width()
        self._apply_typography_for_width(width)

        if not self.dashboardFrame or not self._sidebar or not self._content:
            return

        if width < 860:
            # Amount Layout
            try:
                self._sidebar.grid_forget()
                self._content.grid_forget()
                self.dashboardFrame.grid_columnconfigure(0, weight=1, minsize=0)
                self.dashboardFrame.grid_columnconfigure(1, weight=0, minsize=0)
                self._sidebar.grid(row=1, column=0, padx=16, pady=(8, 8), sticky="nwe")
                self._content.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="nsew")
            except Exception:
                pass
        else:
            # Two Columns Layout
            try:
                self._sidebar.grid_forget()
                self._content.grid_forget()
                self.dashboardFrame.grid_columnconfigure(0, weight=0, minsize=260)
                self.dashboardFrame.grid_columnconfigure(1, weight=1, minsize=0)
                self._sidebar.grid(row=1, column=0, padx=(16, 8), pady=(8, 16), sticky="nsew")
                self._content.grid(row=1, column=1, padx=(8, 16), pady=(8, 16), sticky="nsew")
            except Exception:
                pass


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
