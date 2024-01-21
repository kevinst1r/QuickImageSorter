#utility.py

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPalette, QColor, QBrush, QPainterPath, QPen, QPainter
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

def light_palette():
    palette = QPalette()
    
    palette.setColor(QPalette.Window, QColor(245, 245, 245))  # Light gray background
    palette.setColor(QPalette.WindowText, Qt.black)  # Black text
    palette.setColor(QPalette.Base, QColor(255, 255, 255))  # White base
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))  # Slightly darker than base
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(220, 220, 220))  # Light gray buttons
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(0, 122, 204))  # Blue links
    palette.setColor(QPalette.Highlight, QColor(0, 122, 204))  # Blue highlights
    palette.setColor(QPalette.HighlightedText, Qt.white)

    return palette

def dark_palette_2():
    """
    Create an alternate dark palette for the application.
    """
    palette = QPalette()
    
    palette.setColor(QPalette.Window, QColor(33, 33, 33))  # Darker background
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))  # Darker base
    palette.setColor(QPalette.AlternateBase, QColor(33, 33, 33))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(33, 33, 33))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(255, 165, 0))  # Orange links for contrast
    palette.setColor(QPalette.Highlight, QColor(255, 165, 0))  # Orange highlights
    palette.setColor(QPalette.HighlightedText, Qt.black)

    return palette

def light_palette_2():
    """
    Create an alternate light palette for the application.
    """
    palette = QPalette()
    
    palette.setColor(QPalette.Window, QColor(255, 248, 220))  # Creamy background
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 240))  # Off-white base
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 230))  # Light cream
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(230, 230, 210))  # Soft gray buttons
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(75, 0, 130))  # Indigo links
    palette.setColor(QPalette.Highlight, QColor(75, 0, 130))  # Indigo highlights
    palette.setColor(QPalette.HighlightedText, Qt.white)

    return palette
