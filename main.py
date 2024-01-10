#main.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
import sys
from image_viewer import ImageViewer
from utility import dark_palette

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(dark_palette())

    initialDir = None
    if len(sys.argv) > 1:
        initialDir = sys.argv[1]

    viewer = ImageViewer(initialDir)
    viewer.show()
    sys.exit(app.exec_())

