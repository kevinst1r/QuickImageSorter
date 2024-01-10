#settings.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QCheckBox

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout(self)

        # Checkbox for toggling filename display
        self.filenameCheckbox = QCheckBox("Show Filenames (1)")
        layout.addWidget(self.filenameCheckbox)

        # OK and Cancel buttons
        self.okButton = QPushButton('OK', self)
        self.okButton.clicked.connect(self.accept)
        layout.addWidget(self.okButton)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.reject)
        layout.addWidget(self.cancelButton)