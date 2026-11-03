from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QHBoxLayout,
  QPushButton,
  QLabel,
  QScrollArea,
  QSizePolicy
)

from PyQt6.QtCore import Qt, pyqtSignal

import sqlite3
from functionality.functions.searcher.extractArt import extractAlbumArt

class PlaylistItem(QWidget):
  MAKE_PLAYLIST = pyqtSignal(list)

  def __init__(self, colors, playlistName):
    super().__init__()
    
    self.playlistName = playlistName
    self.colors = colors

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    self.playlistLocations = cursor.execute("SELECT * FROM playlists WHERE playlistName = ?", (self.playlistName,)).fetchall()
    self.playlistList = []
    for song in self.playlistLocations:
      songLocation = song[1]
      songData = cursor.execute("SELECT * FROM songs WHERE location = ?", (songLocation,)).fetchone()
      self.playlistList.append(dict(songData))
    connection.close()

    self.topLayout = QVBoxLayout(self)
    self.topLayout.setContentsMargins(0,0,0,0)

    self.mainWidget = QWidget()
    self.mainLayout = QVBoxLayout(self.mainWidget)
    self.mainLayout.setContentsMargins(0,0,0,0)

    # Playlist name and image
    self.playlistWidget = QWidget()
    self.playlistLayout = QHBoxLayout(self.playlistWidget)

    print("Playlist name: ", self.playlistName)
    playlistImageLocation = self.playlistList[0]["location"]
    playlistImagePixmap = extractAlbumArt(self, playlistImageLocation, 30)
    scaledPlaylistPixmap = playlistImagePixmap.scaled(120,120,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)

    self.playlistImage = QLabel()
    self.playlistImage.setFixedSize(120,120)
    self.playlistImage.setPixmap(scaledPlaylistPixmap)
    self.playlistLayout.addWidget(self.playlistImage)

    # Playlist information #
    self.playlistInformationWidget = QWidget()
    self.playlistInformationLayout = QVBoxLayout(self.playlistInformationWidget)
    self.playlistInformationLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    self.playlistInformationName = QLabel(self.playlistName)
    self.playlistInformationName.setStyleSheet("color: white; font-size:30px; font-weight:700")

    self.playlistInformationLength = QLabel(str(len(self.playlistList)) + " Songs")
    self.playlistInformationLength.setStyleSheet("color: darkgray; font-size:25px; font-weight:700")

    self.playlistInformationLayout.addWidget(self.playlistInformationName)
    self.playlistInformationLayout.addWidget(self.playlistInformationLength)

    self.playlistLayout.addWidget(self.playlistInformationWidget, 1)
    ##

    # Play All Button
    self.playAllWidget = QWidget()
    self.playAllLayout = QVBoxLayout(self.playAllWidget)

    self.playAllButton = QPushButton("Play All")
    self.playAllButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.playAllButton.setFixedSize(120,120)
    self.playAllButton.setStyleSheet(f"background-color: {colors.custom_color_1}; color: white; font-size: 20px; font-weight: 700; border: none; border-radius:10px")

    self.playAllLayout.addWidget(self.playAllButton)
    self.playlistLayout.addWidget(self.playAllWidget)

    self.playAllButton.clicked.connect(lambda: self.MAKE_PLAYLIST.emit(self.playlistList))
    ##
    
    self.mainLayout.addWidget(self.playlistWidget)
    ##
    
    # Scrollable #
    self.scrollableArea = QScrollArea()
    self.scrollableArea.setWidgetResizable(True)
    self.scrollableArea.setStyleSheet("border: none")

    self.scrollableAreaWidget = QWidget()
    self.scrollableAreaLayout = QVBoxLayout(self.scrollableAreaWidget)
    self.scrollableAreaLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.scrollableArea.setWidget(self.scrollableAreaWidget)
    ##

    self.mainLayout.addWidget(self.scrollableArea)
    self.topLayout.addWidget(self.mainWidget)

    self.widgets = []
  
  def createItems(self):
    self.playlistList = sorted(self.playlistList, key=lambda song: song["album"].lower())
    
    for song in self.playlistList:
      songWidget = SongItem(songData = song, colors=self.colors, createPlaylistSignal=self.MAKE_PLAYLIST)
      self.widgets.append(songWidget)
      self.scrollableAreaLayout.addWidget(songWidget)

      song["widget"] = songWidget

class SongItem(QWidget):
  def __init__(self, songData, colors, createPlaylistSignal):
    super().__init__()
    self.setCursor(Qt.CursorShape.PointingHandCursor)
    self.createPlaylistSignal = createPlaylistSignal

    self.topLayout = QVBoxLayout(self)
    self.topLayout.setContentsMargins(0,0,0,0)

    self.songData = songData

    self.mainWidget = QWidget()
    self.mainLayout = QHBoxLayout(self.mainWidget)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.setSpacing(0)

    self.mainWidget.setStyleSheet(f"background-color: {colors.color2}; border-radius:10px")
    self.mainWidget.setFixedHeight(100)

    # Song Image
    self.songImageWidget = QWidget()
    self.songImageWidget.setFixedWidth(100)
    self.songImageLayout = QVBoxLayout(self.songImageWidget)
    
    self.songImage = QLabel()
    self.songImage.setFixedSize(80,80)
    songImagePixmap = extractAlbumArt(self, songData["location"], 40)
    scaledPixmap = songImagePixmap.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.songImage.setPixmap(scaledPixmap)
    
    self.songImageLayout.addWidget(self.songImage)
    self.mainLayout.addWidget(self.songImageWidget)
    ##

    # Name, Artist and Album Widgets
    self.nameArtistAlbumWidget = QWidget()
    self.nameArtistAlbumWidget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred) # Crushes text horizontally, does nothing vertically (fixed height)

    self.nameArtistAlbumLayout = QVBoxLayout(self.nameArtistAlbumWidget)
    self.nameArtistAlbumLayout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
    self.nameArtistAlbumLayout.setContentsMargins(0,0,0,10)

    self.nameWidget = QLabel(str(songData["name"]))
    self.nameWidget.setStyleSheet(f"color: lightgray; font-size: 16px; font-weight:700")
    
    self.artistWidget = QLabel(str(songData["artist"]))
    self.artistWidget.setStyleSheet(f"color: darkgray; font-size: 13px; font-weight:700")

    self.albumWidget = QLabel(songData["album"])
    self.albumWidget.setStyleSheet(f"color: gray; font-size: 11px; font-weight:700")

    self.nameArtistAlbumLayout.addWidget(self.nameWidget)
    self.nameArtistAlbumLayout.addWidget(self.artistWidget)
    self.nameArtistAlbumLayout.addWidget(self.albumWidget)

    self.mainLayout.addWidget(self.nameArtistAlbumWidget)
    #

    self.topLayout.addWidget(self.mainWidget)
  
  def mousePressEvent(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      self.createPlaylistSignal.emit(["single", self.songData])