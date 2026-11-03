from PyQt6.QtWidgets import (
  QWidget,
  QStackedWidget,
  QVBoxLayout,
  QLabel
)

from PyQt6.QtCore import pyqtSignal

from functionality.layouts.stacked.downloadMusic import DownloadWidget
from functionality.layouts.stacked.managePlaylist import ManagePlaylistWidget
from functionality.layouts.stacked.createPlaylist import CreateWidget
from functionality.layouts.stacked.manageMusic import ManageMusicWidget

class MiddleSection(QWidget):
  def __init__(self, colors):
    super().__init__()

    self.middleWidget = QWidget()
    self.middleWidget.setStyleSheet(f"background-color: {colors.color3}")
    self.middleWidget.setContentsMargins(0,0,0,0)
    
    self.middleColumn = QStackedWidget()
    self.middleColumn.setContentsMargins(0,0,0,0)

    self.downloadWidget = DownloadWidget(colors)
    self.middleColumn.addWidget(self.downloadWidget)

    self.managePlaylistWidget = ManagePlaylistWidget(colors)
    self.middleColumn.addWidget(self.managePlaylistWidget)

    self.createWidget = CreateWidget(colors)
    self.middleColumn.addWidget(self.createWidget)

    self.manageMusicWidget = ManageMusicWidget(colors)
    self.middleColumn.addWidget(self.manageMusicWidget)

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.middleWidget)

    self.middleColumn.setCurrentIndex(1)

    self.middleLayout = QVBoxLayout(self.middleWidget)
    self.middleLayout.setContentsMargins(0, 0, 0, 0)
    self.middleLayout.addWidget(self.middleColumn)
  
  def updateStackedWidget(self, status):
    indexes = {"DOWNLOAD MUSIC": 0, "CREATE PLAYLIST": 2, "MANAGE PLAYLIST": 1, "MANAGE MUSIC": 3}
    newIndex = indexes[status]

    print(status)

    self.middleColumn.setCurrentIndex(newIndex)