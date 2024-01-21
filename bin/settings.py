#settings.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QLineEdit, QComboBox
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, settingsManager, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.settingsManager = settingsManager
        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout(self)

        # Checkbox for toggling filename display
        self.filenameCheckbox = QCheckBox("Show Filenames (1)")
        self.filenameCheckbox.setChecked(self.settingsManager.get_setting("show_filenames"))
        layout.addWidget(self.filenameCheckbox)

        # Dropdown for theme selection
        self.themeDropdown = QComboBox()
        self.themeDropdown.addItems(["Dark", "Light", "Dark 2","Light 2"])  # Add more themes as needed
        self.themeDropdown.setCurrentText(self.settingsManager.get_setting("theme"))
        layout.addWidget(QLabel("Theme"))
        layout.addWidget(self.themeDropdown)

        # Dropdown for icon size
        self.iconSizeDropdown = QComboBox()
        self.iconSizeDropdown.addItems(["Small", "Normal", "Large"])
        current_icon_size = settingsManager.get_icon_size()
        if current_icon_size in ["Small", "Normal", "Large"]:
            self.iconSizeDropdown.setCurrentText(current_icon_size)
        else:
            self.iconSizeDropdown.setCurrentText("Normal")  # Default value

        layout.addWidget(QLabel("Icon Size"))
        layout.addWidget(self.iconSizeDropdown)



        # OK and Cancel buttons
        self.okButton = QPushButton('OK', self)
        self.okButton.clicked.connect(self.on_accept)
        layout.addWidget(self.okButton)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.reject)
        layout.addWidget(self.cancelButton)

        # Connect iconSizeDropdown change signal
        self.iconSizeDropdown.currentIndexChanged.connect(self.update_ui_components)

        self.update_ui_components() 

    def update_ui_components(self):
        # Determine font size based on icon size
        icon_size = self.iconSizeDropdown.currentText()
        font_size = {"Small": 8, "Normal": 10, "Large": 15}.get(icon_size, 10)

        # Update font sizes of UI components
        font = self.filenameCheckbox.font()
        font.setPointSize(font_size)
        self.filenameCheckbox.setFont(font)
        self.themeDropdown.setFont(font)
        self.iconSizeDropdown.setFont(font)
        self.okButton.setFont(font)
        self.cancelButton.setFont(font)

    def on_accept(self):
        # Update settings when OK is clicked
        self.settingsManager.set_setting("show_filenames", self.filenameCheckbox.isChecked())
        self.settingsManager.set_setting("theme", self.themeDropdown.currentText())
        self.settingsManager.set_icon_size(self.iconSizeDropdown.currentText())

        # Update UI in the parent window (main image viewer)
        if self.parent():
            self.parent().update_ui_with_settings()
            self.parent().update_font_sizes()  # Update font sizes
            

        self.accept()

class EditHotkeysDialog(QDialog):
    def __init__(self, parent=None):
        super(EditHotkeysDialog, self).__init__(parent)
        self.setWindowTitle('Edit Hotkeys')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout(self)

        # Label for hotkey list
        self.hotkeyListLabel = QLabel("Hotkey List")
        layout.addWidget(self.hotkeyListLabel)

        # OK and Cancel buttons
        self.okButton = QPushButton('OK', self)
        self.okButton.clicked.connect(self.accept)
        layout.addWidget(self.okButton)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.reject)
        layout.addWidget(self.cancelButton)