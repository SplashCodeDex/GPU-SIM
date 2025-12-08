"""
NVIDIA Control Panel Style
Contains NVIDIA brand colors and styling for the fake control panel.
"""

# NVIDIA Brand Colors
NVIDIA_GREEN = "#76B900"
NVIDIA_GREEN_DARK = "#5A8F00"
NVIDIA_GREEN_LIGHT = "#8ED100"
NVIDIA_BLACK = "#1A1A1A"
NVIDIA_DARK_GRAY = "#2D2D2D"
NVIDIA_GRAY = "#404040"
NVIDIA_LIGHT_GRAY = "#666666"
NVIDIA_WHITE = "#FFFFFF"
NVIDIA_TEXT = "#E0E0E0"

# Dark Theme
DARK_THEME = f"""
QMainWindow {{
    background-color: {NVIDIA_BLACK};
}}
QWidget {{
    background-color: {NVIDIA_BLACK};
    color: {NVIDIA_TEXT};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}}
QTreeWidget {{
    background-color: {NVIDIA_DARK_GRAY};
    border: 1px solid {NVIDIA_GRAY};
    border-radius: 4px;
    padding: 5px;
}}
QTreeWidget::item {{
    padding: 8px 5px;
    border-radius: 3px;
}}
QTreeWidget::item:selected {{
    background-color: {NVIDIA_GREEN};
    color: {NVIDIA_WHITE};
}}
QTreeWidget::item:hover {{
    background-color: {NVIDIA_GRAY};
}}
QGroupBox {{
    border: 1px solid {NVIDIA_GRAY};
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 15px;
    font-weight: bold;
    color: {NVIDIA_GREEN};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}}
QPushButton {{
    background-color: {NVIDIA_GRAY};
    border: 1px solid {NVIDIA_LIGHT_GRAY};
    border-radius: 4px;
    padding: 8px 16px;
    color: {NVIDIA_TEXT};
    min-width: 80px;
}}
QPushButton:hover {{
    background-color: {NVIDIA_GREEN};
    color: {NVIDIA_WHITE};
}}
QPushButton:pressed {{
    background-color: {NVIDIA_GREEN_DARK};
}}
QComboBox {{
    background-color: {NVIDIA_DARK_GRAY};
    border: 1px solid {NVIDIA_GRAY};
    border-radius: 4px;
    padding: 5px 10px;
    min-width: 150px;
}}
QComboBox:hover {{
    border-color: {NVIDIA_GREEN};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QSlider::groove:horizontal {{
    height: 6px;
    background: {NVIDIA_GRAY};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {NVIDIA_GREEN};
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}}
QSlider::sub-page:horizontal {{
    background: {NVIDIA_GREEN};
    border-radius: 3px;
}}
QLabel {{
    color: {NVIDIA_TEXT};
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QStatusBar {{
    background-color: {NVIDIA_DARK_GRAY};
    border-top: 1px solid {NVIDIA_GRAY};
    color: {NVIDIA_TEXT};
}}
QMenuBar {{
    background-color: {NVIDIA_DARK_GRAY};
    color: {NVIDIA_TEXT};
}}
QMenuBar::item:selected {{
    background-color: {NVIDIA_GREEN};
}}
QMenu {{
    background-color: {NVIDIA_DARK_GRAY};
    border: 1px solid {NVIDIA_GRAY};
}}
QMenu::item:selected {{
    background-color: {NVIDIA_GREEN};
}}
"""

# Light Theme (for reference, matching real NVIDIA Control Panel)
LIGHT_THEME = f"""
QMainWindow {{
    background-color: #F0F0F0;
}}
QWidget {{
    background-color: #F0F0F0;
    color: #1A1A1A;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}}
QTreeWidget {{
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
}}
QTreeWidget::item:selected {{
    background-color: {NVIDIA_GREEN};
    color: white;
}}
QGroupBox {{
    border: 1px solid #CCCCCC;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 15px;
    font-weight: bold;
    color: {NVIDIA_GREEN_DARK};
}}
QPushButton {{
    background-color: #E0E0E0;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    padding: 8px 16px;
}}
QPushButton:hover {{
    background-color: {NVIDIA_GREEN};
    color: white;
}}
"""

def get_theme(dark_mode: bool = True) -> str:
    """Get the appropriate theme stylesheet."""
    return DARK_THEME if dark_mode else LIGHT_THEME
