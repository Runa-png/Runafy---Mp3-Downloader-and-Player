from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QPainterPath


def drawPlayPixmap():
  canvas = QPixmap(100, 100)
  canvas.fill(Qt.GlobalColor.transparent)

  painter = QPainter(canvas)
  painter.setRenderHint(QPainter.RenderHint.Antialiasing)

  pen = QPen(Qt.GlobalColor.white)
  pen.setWidth(3)
  pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
  painter.setPen(pen)
  painter.setBrush(Qt.BrushStyle.NoBrush)

  path = QPainterPath()

  # Rounded triangle corners
  path.moveTo(20, 10)
  path.lineTo(78, 43)
  path.quadTo(90, 50, 78, 57)
  path.lineTo(20, 90)
  path.quadTo(10, 94, 10, 82)
  path.lineTo(10, 18)
  path.quadTo(10, 6, 20, 10)

  path.closeSubpath()
  painter.drawPath(path)
  painter.end()

  return canvas