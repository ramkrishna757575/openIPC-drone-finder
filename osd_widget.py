# osd_widget.py

import cairo
from PyQt5 import QtWidgets, QtCore, QtGui

from cairo_renderer import CairoRenderer


class OSDWidget(QtWidgets.QWidget):
    def __init__(self, frequency_provider):
        super().__init__()
        self.frequency_provider = frequency_provider
        self.setWindowTitle("Real-Time OSD")
        self.setGeometry(100, 100, 500, 100)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

    def paintEvent(self, event):
        width, height = self.width(), self.height()
        # Fetch the current frequency from the frequency provider
        buzzer_frequency = self.frequency_provider()

        # Use CairoRenderer to create a Cairo surface with the current frequency
        cairo_renderer = CairoRenderer(width, height)
        surface = cairo_renderer.render(buzzer_frequency)

        # Transfer the Cairo surface to a QImage for display
        qimage = QtGui.QImage(
            surface.get_data(), width, height, QtGui.QImage.Format_ARGB32
        )
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, qimage)
        painter.end()

    def update_osd(self):
        self.update()  # Trigger the paintEvent to refresh the display
