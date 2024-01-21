#main.py

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
from PyQt5.QtGui import QIcon
import sys
import os
from bin.image_viewer import ImageViewer
from bin.utility import dark_palette, light_palette, dark_palette_2, light_palette_2
from bin.SettingsManager import SettingsManager


# Ensure the path to the icon is correct
icon_path = os.path.join(os.path.dirname(__file__), 'bin', 'images', 'icon.png')
if not os.path.exists(icon_path):
    raise FileNotFoundError(f"Icon file not found: {icon_path}")


def apply_theme(app, theme):
    if theme == "dark":
        app.setPalette(dark_palette())
    elif theme == "light":
        app.setPalette(light_palette())
    elif theme == "more":
        app.setPalette(dark_palette_2())
    elif theme == "more":
        app.setPalette(light_palette_2())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    trayIcon = QSystemTrayIcon(QIcon('bin/images/icon.png'), app)
    trayIcon.show()
    app.setStyle('Fusion')
    settingsManager = SettingsManager()  # Create the settings manager instance
    apply_theme(app, settingsManager.get_setting("theme"))  
    #app.setPalette(dark_palette())

    initialDir = None
    if len(sys.argv) > 1:
        initialDir = sys.argv[1]

    viewer = ImageViewer(initialDir)
    viewer.show()
    sys.exit(app.exec_())

