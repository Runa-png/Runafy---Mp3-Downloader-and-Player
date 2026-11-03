from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QPainterPath

def drawForwardPixmap():
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

  radius = 5 # This makes the curved corners

  # Triangle One #
  node1 = (10,10)
  path.moveTo(node1[0]+radius,node1[1]+radius)
  
  node2 = (60,50)
  path.lineTo(node2[0]-radius, node2[1]-radius)
  
  path.quadTo(node2[0], node2[1], node2[0]-radius, node2[1]+radius)
  
  node3 = (10,90)
  path.lineTo(node3[0]+radius, node3[1]-radius)

  path.quadTo(node3[0], node3[1], node3[0], node3[1]-radius)
  path.lineTo(node1[0],node1[1]+radius)
  path.quadTo(node1[0], node1[1], node1[0]+radius, node1[1]+radius)
  ##

  # Triangle Two #
  node4 = (40,10)
  path.moveTo(node4[0]+radius,node4[1]+radius)
  
  node5 = (90,50)
  path.lineTo(node5[0]-radius, node5[1]-radius)
  
  path.quadTo(node5[0], node5[1], node5[0]-radius, node5[1]+radius)
  
  node6 = (40,90)
  path.lineTo(node6[0]+radius, node6[1]-radius)

  path.quadTo(node6[0], node6[1], node6[0], node6[1]-radius)
  path.lineTo(node4[0],node4[1]+radius)
  path.quadTo(node4[0], node4[1], node4[0]+radius, node4[1]+radius)
  ##

  #path.closeSubpath()
  painter.drawPath(path)
  painter.end()

  return canvas
