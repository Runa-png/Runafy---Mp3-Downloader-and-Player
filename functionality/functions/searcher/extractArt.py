from mutagen import File
from config import Colors
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QPen, QColor
from PyQt6.QtCore import Qt

def extractAlbumArt(self, location, radius):
  colors = Colors()
  audio = File(location)
  artwork = None

  if "APIC:" in audio.tags:
    artwork = audio.tags["APIC:"].data
  else:
    for tag in audio.tags.values():
      if hasattr(tag, "data") and hasattr(tag, "mime"):
        artwork = tag.data
        break

  if not artwork:
    print("PIXMAP IS NONEXISTANT")    
    return drawInvalidPixmap()

  # Convert the artwork data into a pixmap
  pixmap = QPixmap()
  pixmap.loadFromData(artwork)

  canvas = QPixmap(pixmap.size())
  canvas.fill(Qt.GlobalColor.transparent)

  painter = QPainter(canvas)
  painter.setRenderHint(QPainter.RenderHint.Antialiasing)

  path = QPainterPath()
  path.addRoundedRect(0, 0, canvas.width(), canvas.height(), radius, radius)

  painter.setClipPath(path)

  painter.drawPixmap(0, 0, pixmap)

  # Draw border
  pen = QPen(QColor(Colors.color5))
  pen.setWidth(5)
  painter.setPen(pen)
  painter.setBrush(Qt.BrushStyle.NoBrush)

  borderPath = QPainterPath()
  borderPath.addRoundedRect(
    1, 1,
    canvas.width() - 2,
    canvas.height() - 2,
    radius, radius
  )

  painter.drawPath(borderPath)

  painter.end()
  return canvas

def drawInvalidPixmap():
  canvas = QPixmap(100, 100)
  canvas.fill(Qt.GlobalColor.transparent)

  painter = QPainter(canvas)
  painter.setRenderHint(QPainter.RenderHint.Antialiasing)

  pen = QPen(Qt.GlobalColor.black)
  pen.setWidth(3)
  pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
  painter.setPen(pen)
  painter.setBrush(Qt.BrushStyle.NoBrush)

  path = QPainterPath()

  path.moveTo(25,25)
  path.lineTo(75,75)

  path.moveTo(25,75)
  path.lineTo(75,25)

  painter.drawPath(path)
  painter.end()

  return canvas
