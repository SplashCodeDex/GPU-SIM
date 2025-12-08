import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QLabel, QWidget, QStackedWidget, QHBoxLayout, QMenuBar, QMenu, QAction
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QTimer


class NvidiaControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window icon (path to your icon file)
        self.setWindowIcon(QIcon("C:\\Dell\\Drivers\\log\\294666_nvidia_icon.ico"))  # Replace with actual path to your icon

        self.setWindowTitle("Nvidia Control Panel")
        self.setGeometry(200, 100, 900, 700)  # Set the window size and position

        # Menu Bar Setup
        self.create_menus()

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Sidebar (Tree View)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # Remove the header
        layout.addWidget(self.tree)

        # Add categories to the sidebar and expand them
        self.add_categories()

        # Stacked Widget (Settings Panels)
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Add panels, including the Home page
        self.add_panels()

        # Connect sidebar to panels
        self.tree.currentItemChanged.connect(self.switch_panel)

        # Load watermark image
        self.watermark = QPixmap("C:\\Dell\\Drivers\\log\\nvidia_logo.png")  # Replace with the actual path to your watermark image
        self.scaled_watermark = self.watermark.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Create a timer to repaint the watermark continuously
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.repaint)
        self.timer.start(1000)  # Repaint every second

    def create_menus(self):
        # Create menu bar and items
        menu_bar = self.menuBar()

        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        desktop_menu = QMenu("Desktop", self)
        settings_menu = QMenu("3D Settings", self)
        help_menu = QMenu("Help", self)

        # Add actions to menus
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addAction("Exit")

        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addAction("Preferences")

        desktop_menu.addAction("Change Resolution")
        desktop_menu.addAction("Adjust Desktop Color Settings")

        settings_menu.addAction("Manage 3D Settings")
        settings_menu.addAction("Configure SLI, Surround, PhysX")

        help_menu.addAction("Help")
        help_menu.addAction("About")

        # Add "Created by NVIDIA in 2023" to the Help menu
        help_menu.addAction("NVIDIA info")

        # Add menus to menu bar
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(desktop_menu)
        menu_bar.addMenu(settings_menu)
        menu_bar.addMenu(help_menu)

    def add_categories(self):
        # Sidebar categories
        category_3d = QTreeWidgetItem(["3D Settings"])
        category_display = QTreeWidgetItem(["Display"])
        category_video = QTreeWidgetItem(["Video"])
        category_gpu = QTreeWidgetItem(["GPU Information"])
        category_kb = QTreeWidgetItem(["Keyboard Backlit"])

        # Add subcategories
        category_3d.addChild(QTreeWidgetItem(["Adjust image settings with preview"]))
        category_3d.addChild(QTreeWidgetItem(["Adjust image color"]))
        category_3d.addChild(QTreeWidgetItem(["Calibrate Screen"]))
        category_3d.addChild(QTreeWidgetItem(["Manage 3D settings"]))
        category_3d.addChild(QTreeWidgetItem(["Configure SLI, Surround, PhysX"]))

        category_display.addChild(QTreeWidgetItem(["Change resolution"]))
        category_display.addChild(QTreeWidgetItem(["Adjust desktop color settings"]))
        category_display.addChild(QTreeWidgetItem(["Rotate display"]))

        category_video.addChild(QTreeWidgetItem(["Adjust video color settings"]))
        category_video.addChild(QTreeWidgetItem(["Adjust video image settings"]))

        category_gpu.addChild(QTreeWidgetItem(["GPU Specifications"]))
        category_gpu.addChild(QTreeWidgetItem(["Memory Usage"]))
        category_gpu.addChild(QTreeWidgetItem(["Performance Graph"]))

        category_kb.addChild(QTreeWidgetItem(["Turn on keyboard light"]))
        category_kb.addChild(QTreeWidgetItem(["RGB"]))
        category_kb.addChild(QTreeWidgetItem(["keyboard mapping"]))

        # Add categories to the tree and expand them
        self.tree.addTopLevelItem(category_3d)
        self.tree.addTopLevelItem(category_display)
        self.tree.addTopLevelItem(category_video)
        self.tree.addTopLevelItem(category_gpu)
        self.tree.addTopLevelItem(category_kb)

        # Expand all categories
        self.tree.expandAll()

        # Disable clicking by setting selection mode to NoSelection
        self.tree.setSelectionMode(self.tree.NoSelection)

        # Disable interaction on each item by setting it as not enabled
        self.disable_items(self.tree)

    def disable_items(self, parent_item):
        # Disable all items in the QTreeWidget
        for i in range(parent_item.topLevelItemCount()):
            item = parent_item.topLevelItem(i)
            item.setDisabled(True)  # Disable the item itself
            self.disable_children(item)  # Disable the child items

    def disable_children(self, item):
        for i in range(item.childCount()):
            child_item = item.child(i)
            child_item.setDisabled(True)  # Disable the child item
            self.disable_children(child_item)  # Recursively disable child items

    def add_panels(self):
        # Home Page Panel (Nvidia GTX 2080 Ti)
        home_panel = QWidget()
        home_layout = QVBoxLayout(home_panel)

        # Align the layout to the right
        home_layout.setAlignment(Qt.AlignRight)

        # Nvidia logo (replace 'nvidia_logo.png' with your logo path)
        logo_label = QLabel()
        pixmap = QPixmap("C:\\Dell\\Drivers\\log\\nvidia_logo_2.png")  # Replace with actual logo path
        logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignRight)
        home_layout.addWidget(logo_label)

        # GeForce GTX 780 Ti text
        title_label2 = QLabel("Dell Latitude Gaming")
        title_label2.setFont(QFont("Arial", 14))
        title_label2.setAlignment(Qt.AlignRight)
        home_layout.addWidget(title_label2)

        title_label = QLabel("GeForce GTX 780 Ti (4064MB)")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignRight)
        home_layout.addWidget(title_label)

        # Add GPU specifications
        gpu_info_label = QLabel("CUDA Cores: 4352 | Base Clock: 1350 MHz | Memory Clock: 1750 MHz")
        gpu_info_label.setAlignment(Qt.AlignRight)
        home_layout.addWidget(gpu_info_label)

        # Add driver version info
        driver_info_label = QLabel("Version 332.25.7")
        driver_info_label.setAlignment(Qt.AlignRight)
        home_layout.addWidget(driver_info_label)

        # Add update suggestion with medium font weight and size
        update_info_label = QLabel('<a href="https://www.nvidia.com/en-us/geforce/graphics-cards/16-series/">Update Graphic Driver Version 412.06.2</a> <div>to change settings</div>')
        update_info_label.setFont(QFont("Arial", 12, QFont.Normal))
        update_info_label.setAlignment(Qt.AlignRight)
        update_info_label.setOpenExternalLinks(True)  # Make the link clickable
        home_layout.addWidget(update_info_label)

        # Add empty space for layout spacing
        home_layout.addStretch()

        self.stacked_widget.addWidget(home_panel)

        # Placeholder panels for other settings
        self.panel_3d = QLabel("3D Settings Panel")
        self.panel_display = QLabel("Display Settings Panel")
        self.panel_video = QLabel("Video Settings Panel")
        self.panel_gpu = QLabel("GPU Information Panel")
        self.panel_kb = QLabel("RGB Keyboard Backlit")

        # Add additional panels to the stacked widget
        self.stacked_widget.addWidget(self.panel_3d)
        self.stacked_widget.addWidget(self.panel_display)
        self.stacked_widget.addWidget(self.panel_video)
        self.stacked_widget.addWidget(self.panel_gpu)
        self.stacked_widget.addWidget(self.panel_kb)

    def switch_panel(self, current, previous):
        # Map categories to panels
        mapping = {
            "Adjust image settings with preview": 1,
            "Manage 3D settings": 1,
            "Configure SLI, Surround, PhysX": 1,
            "Change resolution": 2,
            "Adjust desktop color settings": 2,
            "Rotate display": 2,
            "Adjust video color settings": 3,
            "Adjust video image settings": 3,
            "GPU Specifications": 4,
            "Memory Usage": 4,
            "Performance Graph": 4,
            "Adjust Keyboard Light": 5,
            "Keyboard Mapping": 5,
        }
        if current:
            category = current.text(0)
            panel_index = mapping.get(category, 0)
            self.stacked_widget.setCurrentIndex(panel_index)

    def resizeEvent(self, event):
        self.scaled_watermark = self.watermark.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()  # Trigger a repaint
        super().resizeEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        # Paint the watermark image, ensuring it fits the window
        painter = QPainter(self)
        painter.setOpacity(0.1)  # Set opacity for faded watermark
        painter.drawPixmap(self.rect(), self.scaled_watermark)  # Draw the watermark on the window
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NvidiaControlPanel()
    window.show()
    sys.exit(app.exec_())
