from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QPainterPath

def drawShufflePixmap():
  canvas = QPixmap(100, 100)
  canvas.fill(Qt.GlobalColor.transparent)

  painter = QPainter(canvas)
  painter.setRenderHint(QPainter.RenderHint.Antialiasing)

  pen = QPen(Qt.GlobalColor.black)
  pen.setWidth(4)
  pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
  painter.setPen(pen)
  painter.setBrush(Qt.BrushStyle.NoBrush)

  path = QPainterPath()

  radius = 4

  # Arrow 1
  node1 = (10,25)
  node2 = (60, 25)
  node3 = (45,10)
  node4 = (60,10)
  node5 = (90,40)
  node6 = (10,40)

  path.moveTo(node1[0]+radius, node1[1])
  path.lineTo(node2[0]-radius, node2[1])
  path.quadTo(node2[0], node2[1], node2[0]-radius, node2[1]-radius)
  path.lineTo(node3[0]+radius, node3[1]+radius)
  path.quadTo(node3[0], node3[1], node3[0]+radius, node3[1])
  path.lineTo(node4[0], node4[1])
  path.quadTo(node4[0], node4[1], node4[0]+radius, node4[1]+radius)
  path.lineTo(node5[0]-radius, node5[1]-radius)
  path.quadTo(node5[0], node5[1], node5[0]-radius, node5[1])
  path.lineTo(node6[0]+radius, node6[1])
  path.quadTo(node6[0], node6[1], node6[0], node6[1]-radius)
  path.lineTo(node1[0], node1[1]+radius)
  path.quadTo(node1[0], node1[1], node1[0]+radius, node1[1])

  # Arrow 2
  node1 = (90, 75)
  node2 = (40, 75)
  node3 = (55, 90)
  node4 = (40, 90)
  node5 = (10, 60)
  node6 = (90, 60)

  path.moveTo(node1[0] - radius, node1[1])
  path.lineTo(node2[0] + radius, node2[1])
  path.quadTo(node2[0], node2[1], node2[0] + radius, node2[1] + radius)
  path.lineTo(node3[0] - radius, node3[1] - radius)
  path.quadTo(node3[0], node3[1], node3[0] - radius, node3[1])
  path.lineTo(node4[0], node4[1])
  path.quadTo(node4[0], node4[1], node4[0] - radius, node4[1] - radius)
  path.lineTo(node5[0] + radius, node5[1] + radius)
  path.quadTo(node5[0], node5[1], node5[0] + radius, node5[1])
  path.lineTo(node6[0] - radius, node6[1])
  path.quadTo(node6[0], node6[1], node6[0], node6[1] + radius)
  path.lineTo(node1[0], node1[1] - radius)
  path.quadTo(node1[0], node1[1], node1[0] - radius, node1[1])

  painter.drawPath(path)
  painter.end()

  return canvas