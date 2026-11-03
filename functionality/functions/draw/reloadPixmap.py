from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QPainterPath

def drawReloadPixmap():
  canvas = QPixmap(100, 100)
  canvas.fill(Qt.GlobalColor.transparent)

  painter = QPainter(canvas)
  painter.setRenderHint(QPainter.RenderHint.Antialiasing)

  pen = QPen(Qt.GlobalColor.white)
  pen.setWidth(4)
  pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
  painter.setPen(pen)
  painter.setBrush(Qt.BrushStyle.NoBrush)

  triangleSideWidth = 10

  path = QPainterPath()

  path.moveTo(10+triangleSideWidth,50-triangleSideWidth) # Left side
  path.quadTo(10+triangleSideWidth,10, 50,10) # Top of the shape
  path.quadTo(90,10, 90,50) # Right Side
  path.quadTo(90,90, 50,90) # Bottom
  path.quadTo(10+triangleSideWidth,90, 10+triangleSideWidth,60) # Left side, with space removed for triangle

  # Draw the triangle
  path.lineTo(10, 60)
  path.lineTo(25, 50)
  path.lineTo(40, 60)
  path.lineTo(30, 60)

  # Go back around
  path.moveTo(10+triangleSideWidth,50-triangleSideWidth)
  path.lineTo(20+triangleSideWidth, 50-triangleSideWidth)
  
  path.quadTo(20+triangleSideWidth,20, 50,20) # Top of the shape
  path.quadTo(80,20, 80,50) # Right Side
  path.quadTo(80,80, 50,80) # Bottom
  path.quadTo(20+triangleSideWidth,80, 20+triangleSideWidth,60) # Left side, with space removed for triangle

  painter.drawPath(path)
  painter.end()

  return canvas