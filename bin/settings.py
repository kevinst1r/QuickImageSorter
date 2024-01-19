#settings.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QCheckBox, QLineEdit

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

        # OK and Cancel buttons
        self.okButton = QPushButton('OK', self)
        self.okButton.clicked.connect(self.on_accept)
        layout.addWidget(self.okButton)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.reject)
        layout.addWidget(self.cancelButton)

    def on_accept(self):
        # Update settings when OK is clicked
        self.settingsManager.set_setting("show_filenames", self.filenameCheckbox.isChecked())
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