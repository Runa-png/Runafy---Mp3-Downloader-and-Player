from PyQt6.QtCore import (
  Qt
)

from PyQt6.QtWidgets import (
  QWidget,
  QHBoxLayout,
  QVBoxLayout,
  QLabel,
  QApplication
)

from config import Colors

from functionality.layouts.left import LeftSection
from functionality.layouts.middle import MiddleSection
from functionality.layouts.bottom import BottomSection
from functionality.layouts.top import TopSection

from functionality.layouts.stacked.playlistItem import PlaylistItem

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.setSpacing(0)

    self.setMinimumWidth(670)

    self.colors = Colors()
    
    self.leftColumn = LeftSection(self.colors)
    self.leftColumn.UPDATE_STACKED_WIDGET.connect(lambda playlistName: self.createStackedWidgetItem(playlistName))
    
    self.middleColumn = MiddleSection(self.colors)
    self.middleColumn.createWidget.PLAYLIST_CREATED.connect(lambda: self.leftColumn.reload())
    self.middleColumn.manageMusicWidget.SONG_DELETED.connect(lambda: self.leftColumn.reload()) # Empty playlist should not be shown
    
    self.middleColumn.managePlaylistWidget.UPDATE_LEFT_BAR.connect(lambda: self.leftColumn.reload())
    self.middleColumn.managePlaylistWidget.SET_STACKED_WIDGET.connect(lambda playlistName: self.createStackedWidgetItem(playlistName))
    
    def playlistUpdated():
      self.middleColumn.managePlaylistWidget.showEvent()
      self.leftColumn.reload()
    
    self.middleColumn.managePlaylistWidget.UPDATE_PLAYLIST.connect(lambda: playlistUpdated())

    self.bottomSection = BottomSection(self.colors)

    self.topSection = TopSection(self.colors)
    self.topSection.DROPDOWN_PRESSED.connect(lambda status: self.middleColumn.updateStackedWidget(status))

    # Center section
    self.centerLayout = QHBoxLayout()
    self.centerLayout.addWidget(self.leftColumn)
    self.centerLayout.addWidget(self.middleColumn, stretch=1)

    # Row widgets
    self.bottomLayout = QHBoxLayout()
    self.bottomLayout.addWidget(self.bottomSection)

    self.topLayout = QHBoxLayout()
    self.topLayout.addWidget(self.topSection)

    # Add widgets
    self.mainLayout.addLayout(self.topLayout)
    self.mainLayout.addLayout(self.centerLayout, stretch=1)
    self.mainLayout.addLayout(self.bottomLayout)

    # Variables
    self.currentWidget = None
    self.playlistWidgets = {}
  
  def closeEvent(self, event):
    print("Please wait for the threads to clear!")

    # Put methods to end the multithreads here
    self.middleColumn.downloadWidget.killWorker()

    event.accept()
    QApplication.quit()
  
  def createStackedWidgetItem(self, playlistName):
    if self.playlistWidgets.get(playlistName):
      self.middleColumn.middleColumn.setCurrentWidget(self.playlistWidgets[playlistName])
      return
    
    print("Creating a new widget")
    widget = PlaylistItem(colors=self.colors, playlistName=playlistName)
    widget.MAKE_PLAYLIST.connect(lambda data: self.bottomSection.writePlaylist(data))
    widget.createItems()
    
    self.playlistWidgets[playlistName] = widget
    
    self.middleColumn.middleColumn.addWidget(widget)
    self.middleColumn.middleColumn.setCurrentWidget(widget)
