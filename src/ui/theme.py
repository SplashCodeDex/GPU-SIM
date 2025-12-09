"""
GPU-SIM UI Theme Definitions
Defines the color palette, fonts, and stylesheets for the professional dark theme.
"""

from PyQt5.QtGui import QColor, QFont

class Theme:
    # Color Palette
    COLOR_ACCENT = "#76b900"        # NVIDIA Green
    COLOR_ACCENT_HOVER = "#8bc34a"  # Lighter Green
    COLOR_BACKGROUND = "#1e1e1e"    # Dark Background
    COLOR_SURFACE = "#2d2d2d"       # Card/Panel Background
    COLOR_SURFACE_HOVER = "#3d3d3d" # Card/Panel Hover
    COLOR_BORDER = "#3d3d3d"        # Border Color
    COLOR_TEXT_PRIMARY = "#ffffff"  # Primary Text
    COLOR_TEXT_SECONDARY = "#888888" # Secondary Text / Labels
    COLOR_DANGER = "#f44336"        # Error/Danger (Red)
    COLOR_SUCCESS = "#4caf50"       # Success (Green)
    COLOR_WARNING = "#ff9800"       # Warning (Orange)
    COLOR_INFO = "#2196f3"          # Info (Blue)

    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_HEADER_SIZE = 24
    FONT_SUBHEADER_SIZE = 16
    FONT_BODY_SIZE = 14
    FONT_SMALL_SIZE = 11

    # Stylesheets

    # Main Window
    STYLE_MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {COLOR_BACKGROUND};
        }}
        QWidget {{
            color: {COLOR_TEXT_PRIMARY};
            font-family: "{FONT_FAMILY}";
            font-size: {FONT_BODY_SIZE}px;
        }}
    """

    # Buttons
    STYLE_BUTTON_PRIMARY = f"""
        QPushButton {{
            background-color: {COLOR_ACCENT};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLOR_ACCENT_HOVER};
        }}
        QPushButton:pressed {{
            background-color: #558b00;
        }}
        QPushButton:disabled {{
            background-color: {COLOR_SURFACE_HOVER};
            color: {COLOR_TEXT_SECONDARY};
        }}
    """

    STYLE_BUTTON_SECONDARY = f"""
        QPushButton {{
            background-color: {COLOR_SURFACE};
            color: {COLOR_TEXT_PRIMARY};
            border: 1px solid {COLOR_BORDER};
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {COLOR_SURFACE_HOVER};
            border-color: {COLOR_TEXT_SECONDARY};
        }}
        QPushButton:pressed {{
            background-color: #1a1a1a;
        }}
    """

    STYLE_BUTTON_DANGER = f"""
        QPushButton {{
            background-color: transparent;
            color: {COLOR_DANGER};
            border: 1px solid {COLOR_DANGER};
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: rgba(244, 67, 54, 0.1);
        }}
    """

    # Cards (QFrame)
    STYLE_CARD = f"""
        QFrame {{
            background-color: {COLOR_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: 8px;
        }}
    """

    # Sidebar / Navigation
    STYLE_SIDEBAR = f"""
        QListWidget {{
            background-color: {COLOR_SURFACE};
            border: none;
            outline: none;
        }}
        QListWidget::item {{
            padding: 12px;
            border-radius: 4px;
        }}
        QListWidget::item:selected {{
            background-color: {COLOR_ACCENT};
            color: white;
        }}
        QListWidget::item:hover:!selected {{
            background-color: {COLOR_SURFACE_HOVER};
        }}
    """

    # Inputs
    STYLE_COMBOBOX = f"""
        QComboBox {{
            background-color: {COLOR_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: 4px;
            padding: 6px;
            color: {COLOR_TEXT_PRIMARY};
        }}
        QComboBox:hover {{
            border-color: {COLOR_ACCENT};
        }}
        QComboBox::drop-down {{
            border: none;
        }}
    """
