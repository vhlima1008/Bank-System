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

