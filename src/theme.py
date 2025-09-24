# theme.py
# ---------------------- Theme/Colors ----------------------
PRIMARY_BG = "#353941"
SURFACE_BG = "#26282B"
ACCENT     = "#5F85DB"
TEXT       = "#D1E3FF"
BORDER     = "#26282B"

ALERT_RED       = "#EF4444"  
ALERT_RED_SOFT  = "#FCA5A5"  
ALERT_RED_DARK  = "#7F1D1D"  

def darker(hex_color: str, factor: float = 0.85) -> str:
    """Escurece a cor para usar no hover"""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return f"#{r:02x}{g:02x}{b:02x}"

# já define aqui para ser importado direto
ACCENT_HOVER = darker(ACCENT, 0.78)