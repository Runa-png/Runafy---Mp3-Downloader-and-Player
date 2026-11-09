from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QLabel,
  QScrollArea,
  QPushButton
)

from PyQt6.QtCore import (Qt, pyqtSignal)

from PyQt6.QtGui import QIcon

from functionality.functions.playlists.readPlaylists import readPlaylists
from functionality.functions.searcher.extractArt import extractAlbumArt

class LeftSection(QWidget):
  UPDATE_STACKED_WIDGET = pyqtSignal(str)
  
  def __init__(self, colors):
    super().__init__()

    self.colors = colors

    self.leftWidget = QWidget()
    self.leftWidget.setStyleSheet(f"background-color: {colors.color2}")
    self.leftWidget.setFixedWidth(90)
    self.leftColumn = QVBoxLayout(self.leftWidget)
    self.leftColumn.setContentsMargins(0,0,0,0)

    self.scrollableArea = QScrollArea()
    self.scrollableArea.setWidgetResizable(True)
    self.scrollableArea.setStyleSheet("border: none")

    self.scrollableArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) # Disable horizontal scrolling
    
    self.scrollableAreaWidget = QWidget()
    
    self.scrollableAreaLayout = QVBoxLayout(self.scrollableAreaWidget)
    self.scrollableAreaLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    self.scrollableArea.setWidget(self.scrollableAreaWidget)

    self.leftColumn.addWidget(self.scrollableArea)

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.leftWidget)

    # Variables
    self.playlists = {}
    self.selectedPlaylist = None
  
  def showEvent(self, event):
    print("Left Bar Showing")

    self.reload()
    
  def reload(self): # Reloads the Left Bars album list
    print("reloading left bar")
    self.purgeWidgets()
    self.readPlaylists() # Create a dict of each playlist, stored in self
    self.createWidgets() # Create a widget for each playlist, stored in each playlist dict
  
  def readPlaylists(self):
    self.playlists = readPlaylists()

  def purgeWidgets(self):
    for playlist in self.playlists:
      widget = self.playlists[playlist][0]["widget"]
      widget.hide()
  
  def createWidgets(self):
    for playlistName in self.playlists:
      firstSong = self.playlists[playlistName][0] # The first song in the playlist, use for album icon

      albumWidget = AlbumSelection(parent=self, albumImageLocation=firstSong["location"], playlistName=playlistName, colors=self.colors)
      self.scrollableAreaLayout.addWidget(albumWidget)

      albumWidget.PLAYLIST_SELECTED.connect(lambda playlistName: self.playlistButtonPressed(playlistName=playlistName))

      self.playlists[playlistName][0]["widget"] = albumWidget
  
  def playlistButtonPressed(self, playlistName):
    if self.selectedPlaylist:
      self.playlists[self.selectedPlaylist][0]["widget"].albumImage.setStyleSheet(f"background-color: none")
    
    self.UPDATE_STACKED_WIDGET.emit(playlistName)
    self.selectedPlaylist = playlistName

    self.playlists[playlistName][0]["widget"].albumImage.setStyleSheet(f"background-color: {self.colors.color6}")


class AlbumSelection(QWidget):
  PLAYLIST_SELECTED = pyqtSignal(str)
  
  def __init__(self, parent, albumImageLocation, playlistName, colors):
    super().__init__()

    self.topLayout = QVBoxLayout(self)
    self.topLayout.setContentsMargins(0,0,0,0)
    self.topLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.mainWidget = QWidget()
    self.mainLayout = QVBoxLayout(self.mainWidget)
    self.mainLayout.setContentsMargins(0,0,0,0)

    albumPixmap = extractAlbumArt(self, albumImageLocation, 30)
    self.albumImage = QPushButton()
    self.albumImage.setFixedSize(65,65)
    self.albumImage.setCursor(Qt.CursorShape.PointingHandCursor)
    if albumPixmap != None:
      scaledIcon = albumPixmap.scaled(65,65,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
      self.albumImage.setIcon(QIcon(scaledIcon))
      self.albumImage.setIconSize(scaledIcon.size())

    self.topLayout.addWidget(self.albumImage)
    self.topLayout.addWidget(self.mainWidget)

    self.albumImage.clicked.connect(lambda: self.PLAYLIST_SELECTED.emit(playlistName))