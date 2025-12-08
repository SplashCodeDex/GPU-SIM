"""
GeForce Experience - Style Definitions
Modern dark theme matching the real GeForce Experience app.
"""

# NVIDIA Brand Colors
GFE_GREEN = "#76B900"
GFE_GREEN_HOVER = "#8AC926"
GFE_GREEN_DARK = "#5A8C00"

GFE_BLACK = "#1A1A1A"
GFE_DARK_GRAY = "#242424"
GFE_MEDIUM_GRAY = "#2D2D2D"
GFE_LIGHT_GRAY = "#3D3D3D"
GFE_TEXT = "#FFFFFF"
GFE_TEXT_SECONDARY = "#A0A0A0"
GFE_TEXT_MUTED = "#666666"

GFE_ACCENT_BLUE = "#00A3E0"
GFE_ACCENT_RED = "#FF5A5A"
GFE_ACCENT_YELLOW = "#FFB800"


def get_gfe_stylesheet() -> str:
    """Return the GeForce Experience dark theme stylesheet."""
    return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {GFE_BLACK};
        }}

        QWidget {{
            background-color: {GFE_BLACK};
            color: {GFE_TEXT};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
        }}

        /* Menu Bar */
        QMenuBar {{
            background-color: {GFE_DARK_GRAY};
            color: {GFE_TEXT};
            border: none;
            padding: 5px;
        }}

        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: 4px;
        }}

        QMenuBar::item:selected {{
            background-color: {GFE_LIGHT_GRAY};
        }}

        QMenu {{
            background-color: {GFE_MEDIUM_GRAY};
            border: 1px solid {GFE_LIGHT_GRAY};
            border-radius: 4px;
            padding: 5px;
        }}

        QMenu::item {{
            padding: 8px 30px 8px 15px;
            border-radius: 3px;
        }}

        QMenu::item:selected {{
            background-color: {GFE_GREEN};
        }}

        /* Scroll Bars */
        QScrollBar:vertical {{
            background: {GFE_DARK_GRAY};
            width: 10px;
            border-radius: 5px;
        }}

        QScrollBar::handle:vertical {{
            background: {GFE_LIGHT_GRAY};
            border-radius: 5px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {GFE_GREEN};
        }}

        QScrollBar:horizontal {{
            background: {GFE_DARK_GRAY};
            height: 10px;
            border-radius: 5px;
        }}

        QScrollBar::handle:horizontal {{
            background: {GFE_LIGHT_GRAY};
            border-radius: 5px;
            min-width: 30px;
        }}

        /* Buttons */
        QPushButton {{
            background-color: {GFE_GREEN};
            color: {GFE_BLACK};
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            font-weight: 600;
        }}

        QPushButton:hover {{
            background-color: {GFE_GREEN_HOVER};
        }}

        QPushButton:pressed {{
            background-color: {GFE_GREEN_DARK};
        }}

        QPushButton:disabled {{
            background-color: {GFE_LIGHT_GRAY};
            color: {GFE_TEXT_MUTED};
        }}

        QPushButton[secondary="true"] {{
            background-color: transparent;
            border: 2px solid {GFE_GREEN};
            color: {GFE_GREEN};
        }}

        QPushButton[secondary="true"]:hover {{
            background-color: rgba(118, 185, 0, 0.1);
        }}

        /* Labels */
        QLabel {{
            background: transparent;
            color: {GFE_TEXT};
        }}

        QLabel[header="true"] {{
            font-size: 24px;
            font-weight: bold;
        }}

        QLabel[subheader="true"] {{
            font-size: 14px;
            color: {GFE_TEXT_SECONDARY};
        }}

        /* Cards */
        QFrame[card="true"] {{
            background-color: {GFE_DARK_GRAY};
            border-radius: 8px;
            padding: 15px;
        }}

        QFrame[card="true"]:hover {{
            background-color: {GFE_MEDIUM_GRAY};
        }}

        /* Tabs */
        QTabWidget::pane {{
            background-color: {GFE_BLACK};
            border: none;
        }}

        QTabBar::tab {{
            background-color: transparent;
            color: {GFE_TEXT_SECONDARY};
            padding: 12px 20px;
            border: none;
            border-bottom: 3px solid transparent;
            font-weight: 500;
        }}

        QTabBar::tab:selected {{
            color: {GFE_GREEN};
            border-bottom: 3px solid {GFE_GREEN};
        }}

        QTabBar::tab:hover {{
            color: {GFE_TEXT};
        }}

        /* Progress Bars */
        QProgressBar {{
            background-color: {GFE_DARK_GRAY};
            border: none;
            border-radius: 4px;
            height: 8px;
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {GFE_GREEN};
            border-radius: 4px;
        }}

        /* Line Edits */
        QLineEdit {{
            background-color: {GFE_MEDIUM_GRAY};
            border: 1px solid {GFE_LIGHT_GRAY};
            border-radius: 4px;
            padding: 8px 12px;
            color: {GFE_TEXT};
        }}

        QLineEdit:focus {{
            border: 1px solid {GFE_GREEN};
        }}

        /* Combo Boxes */
        QComboBox {{
            background-color: {GFE_MEDIUM_GRAY};
            border: 1px solid {GFE_LIGHT_GRAY};
            border-radius: 4px;
            padding: 8px 12px;
            color: {GFE_TEXT};
        }}

        QComboBox:hover {{
            border: 1px solid {GFE_GREEN};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {GFE_MEDIUM_GRAY};
            border: 1px solid {GFE_LIGHT_GRAY};
            selection-background-color: {GFE_GREEN};
        }}

        /* Check Boxes */
        QCheckBox {{
            color: {GFE_TEXT};
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 3px;
            border: 2px solid {GFE_LIGHT_GRAY};
        }}

        QCheckBox::indicator:checked {{
            background-color: {GFE_GREEN};
            border: 2px solid {GFE_GREEN};
        }}

        /* Sliders */
        QSlider::groove:horizontal {{
            background: {GFE_DARK_GRAY};
            height: 6px;
            border-radius: 3px;
        }}

        QSlider::handle:horizontal {{
            background: {GFE_GREEN};
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }}

        QSlider::sub-page:horizontal {{
            background: {GFE_GREEN};
            border-radius: 3px;
        }}

        /* Status Bar */
        QStatusBar {{
            background-color: {GFE_DARK_GRAY};
            color: {GFE_TEXT_SECONDARY};
            border-top: 1px solid {GFE_LIGHT_GRAY};
        }}
    """
