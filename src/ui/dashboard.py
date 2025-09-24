import customtkinter as ctk
from theme import PRIMARY_BG, SURFACE_BG, TEXT, ACCENT, ACCENT_HOVER, BORDER, ALERT_RED_SOFT, ALERT_RED_DARK, darker
from clientAccount import ClientAccount

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, on_logout, username="Cliente"):
        super().__init__(master, corner_radius=18, fg_color=SURFACE_BG)
        self.on_logout = on_logout
        self.usernameVar = username

        self.account = ClientAccount(owner=username)
        
        self._sidebar = None
        self._content = None
        self.balanceLbl = None
        self.dynamicArea = None
        
        self._build_ui()

    def _build_ui(self):
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

    def _clear_dynamic(self):
        for w in self.dynamicArea.winfo_children():
            w.destroy()

    def _render_welcome(self):
        self._clear_dynamic()
        ctk.CTkLabel(self.dynamicArea, text="Bem-vindo!", text_color=TEXT).pack(pady=20)

    def showDeposit(self):
        self._clear_dynamic()
        entry = ctk.CTkEntry(self.dynamicArea, placeholder_text="Valor do depósito")
        entry.pack(pady=10)

        def do_deposit():
            try:
                val = float(entry.get())
                self.account.deposit(val)
                self.balanceLbl.configure(text=f"R$ {self.account.balance:,.2f}")
                self.showExtract()
            except Exception as e:
                ctk.CTkLabel(self.dynamicArea, text=f"Erro: {e}", text_color="red").pack()

        ctk.CTkButton(self.dynamicArea, text="Confirmar", command=do_deposit).pack(pady=10)

    def showWithdraw(self):
        self._clear_dynamic()
        entry = ctk.CTkEntry(self.dynamicArea, placeholder_text="Valor do saque")
        entry.pack(pady=10)

        def do_withdraw():
            try:
                val = float(entry.get())
                self.account.withdraw(val)
                self.balanceLbl.configure(text=f"R$ {self.account.balance:,.2f}")
                self.showExtract()
            except Exception as e:
                ctk.CTkLabel(self.dynamicArea, text=f"Erro: {e}", text_color="red").pack()

        ctk.CTkButton(self.dynamicArea, text="Confirmar", command=do_withdraw).pack(pady=10)

    def showExtract(self):
        self._clear_dynamic()
        for mov in self.account.get_extract():
            ctk.CTkLabel(self.dynamicArea, text=mov, text_color=TEXT).pack(anchor="w")