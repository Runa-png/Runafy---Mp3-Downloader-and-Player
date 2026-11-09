from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QPainterPath

def drawPausePixmap():
  canvas = QPixmap(100, 100)
  canvas.fill(Qt.GlobalColor.transparent)

  painter = QPainter(canvas)
  painter.setRenderHint(QPainter.RenderHint.Antialiasing)

  pen = QPen(Qt.GlobalColor.black)
  pen.setWidth(3)
  pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
  painter.setPen(pen)
  painter.setBrush(Qt.BrushStyle.NoBrush)

  radius = 5

  painter.drawRoundedRect(10,10, 20,80, radius, radius)
  painter.drawRoundedRect(70,10, 20,80, radius, radius)

  return canvas