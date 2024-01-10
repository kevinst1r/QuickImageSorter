#utility.py

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPalette, QColor, QBrush, QPainterPath, QPen, QPainter
from PyQt5.QtCore import Qt

def dark_palette():
    """
    Create a dark palette for the application.
    """
    palette = QPalette()
    
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    return palette

class OutlinedLabel(QLabel):
    def __init__(self, parent=None):
        super(OutlinedLabel, self).__init__(parent)
        self.outlineWidth = 8
        self.outlineColor = QColor('black')
        self.textColor = QColor('white')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Adjust the start position to account for the outline width
        start_x = self.outlineWidth

        # Adjust the Y-coordinate to lower the text slightly
        start_y = self.outlineWidth + self.font().pointSizeF() + 3  # Increase the value to move text down

        # Text path
        path = QPainterPath()
        font = self.font()
        path.addText(start_x, start_y, font, self.text())

        # Outline
        painter.setPen(QPen(self.outlineColor, self.outlineWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(self.textColor)
        painter.drawPath(path)

        # Text fill
        painter.fillPath(path, QBrush(self.textColor))