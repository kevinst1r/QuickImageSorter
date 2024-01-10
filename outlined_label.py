#outlined_label.py

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush, QPainterPath, QPen
from PyQt5.QtCore import Qt

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