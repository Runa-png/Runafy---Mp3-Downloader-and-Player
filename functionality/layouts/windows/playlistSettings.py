from PyQt6.QtWidgets import (
  QWidget,
  QLabel,
  QVBoxLayout,
  QHBoxLayout,
  QScrollArea,
  QPushButton,
  QSizePolicy
)

from PyQt6.QtCore import Qt, pyqtSignal

from sqlite3 import connect, Row
from config import Colors
from copy import copy

from functionality.functions.searcher.extractArt import extractAlbumArt

class playlistSettingsWidget(QWidget):
  PLAYLIST_UPDATED = pyqtSignal()
  
  def __init__(self, playlistName):
    super().__init__()
    self.playlistName = playlistName
    self.colors = Colors()

    self.setStyleSheet(f"background-color: {self.colors.color3}")

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)

    self.topWidget = QWidget()
    self.topLayout = QVBoxLayout(self.topWidget)
    self.topLayout.setContentsMargins(0,0,0,0)
    self.topLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    # Playlist Name #
    self.playlistNameWidget = QWidget()
    self.playlistNameWidget.setFixedHeight(60)
    self.playlistNameWidget.setStyleSheet(f"background-color:{self.colors.color1}")
    self.playlistNameLayout = QVBoxLayout(self.playlistNameWidget)
    self.playlistNameLayout.setContentsMargins(0,0,0,0)
    self.playlistNameLabel = QLabel(self.playlistName)
    self.playlistNameLabel.setStyleSheet("color:white; font-size:25px; font-weight:800; text-decoration:underline")
    self.playlistNameLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.playlistNameLayout.addWidget(self.playlistNameLabel)
    self.topLayout.addWidget(self.playlistNameWidget, stretch=1)
    
    self.mainLayout.addWidget(self.topWidget, 1)
    ##

    # Scrollable Area #
    self.scrollableArea = QScrollArea()
    self.scrollableArea.setStyleSheet("border: none;")

    self.scrollableWidget = QWidget()
    self.scrollableLayout = QVBoxLayout(self.scrollableWidget)
    self.scrollableLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.scrollableArea.setWidgetResizable(True)
    self.scrollableArea.setWidget(self.scrollableWidget)
    self.topLayout.addWidget(self.scrollableArea)
    ##

    # Add button #
    self.addButtonWidget = QWidget()
    self.addButtonLayout = QVBoxLayout(self.addButtonWidget)
    self.addButton = QPushButton("Commit!")
    self.addButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.addButton.setFixedHeight(25)
    self.addButton.setStyleSheet(f"background-color: {self.colors.color2}; font-size:13px; font-weight:800; color: white; border:none; border-radius:5px")
    self.addButtonLayout.addWidget(self.addButton)
    self.topLayout.addWidget(self.addButtonWidget)

    self.addButton.clicked.connect(lambda: self.commitButtonPressed())
    ##

    ## THE REST IS IN FUNCTION createWidgetsForEachSong

    # Variables #
    self.widgets = []
  
  def commitButtonPressed(self):
    self.connection.commit()
    self.PLAYLIST_UPDATED.emit()
    self.addButton.setStyleSheet(f"background-color: {self.colors.color2}; font-size:13px; font-weight:800; color: lime; border:none; border-radius:5px")
  
  def showEvent(self, *args):
    self.playlistData = self.fetchSongsOutsideOfPlaylist()
    self.createWidgetsForEachSong()
  
  def closeEvent(self, *args):
    self.connection.close()
  
  def fetchSongsOutsideOfPlaylist(self):
    def convertRowData(data: dict):
      songData = self.cursor.execute("SELECT * FROM songs WHERE location = ?", (data["location"],)).fetchone()
      return dict(songData)
    
    self.connection = connect("database.db")
    self.cursor = self.connection.cursor()
    self.cursor.row_factory = Row

    playlistLocations = self.cursor.execute("SELECT location FROM playlists WHERE playlistName = ?", (self.playlistName,)).fetchall()
    playlistLocations = list(map(dict, playlistLocations))

    playlistSongs = list(map(convertRowData, playlistLocations))

    allSongs = self.cursor.execute("SELECT * FROM songs").fetchall()
    allSongs = list(map(dict, allSongs))

    totalSongData = [] # Store dicts of all songs, in playlist and not
    for song in allSongs:
      if song in playlistSongs:
        songData = {"inplaylist": True, "data": song, "playlistName": self.playlistName}
      else:
        songData = {"inplaylist": False, "data": song, "playlistName": self.playlistName}
      totalSongData.append(songData)

    sortedTotalSongData = sorted(totalSongData, key=lambda song: song["data"]["album"].lower())
    return sortedTotalSongData

  def createWidgetsForEachSong(self):
    for song in self.playlistData:
      newWidget = songWidget(song, self.colors, [self.connection, self.cursor])
      self.scrollableLayout.addWidget(newWidget)
      self.widgets.append(newWidget)

class songWidget(QWidget):
  def __init__(self, songData, colors, connectionData):
    super().__init__()

    self.songData = songData
    self.colors = colors
    self.setFixedHeight(120)

    self.connection, self.cursor = connectionData

    self.topLayout = QVBoxLayout(self)

    self.mainWidget = QWidget()
    self.mainWidget.setStyleSheet(f"background-color:{colors.color2}; border-radius:10px")
    self.mainLayout = QHBoxLayout(self.mainWidget)

    self.albumImage = QLabel()
    albumArtPixmap = extractAlbumArt(self, self.songData["data"]["location"], 20)
    scaledAlbumArtPixmap = albumArtPixmap.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.albumImage.setPixmap(scaledAlbumArtPixmap)
    self.mainLayout.addWidget(self.albumImage)

    # Song Data #
    self.songInfoWidget = QWidget()
    self.songInfoWidget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred) # Crushes text horizontally, does nothing vertically (fixed height)
    self.songInfoLayout = QVBoxLayout(self.songInfoWidget)
    self.songInfoLayout.setContentsMargins(0,0,0,0)
    self.songInfoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    self.songName = QLabel(self.songData["data"]["name"])
    self.songName.setStyleSheet("color: white; font-size:15px; font-weight:600")
    self.songInfoLayout.addWidget(self.songName,1)
    self.artistName = QLabel(self.songData["data"]["artist"])
    self.artistName.setStyleSheet("color: darkgray; font-size:13px; font-weight:600")
    self.songInfoLayout.addWidget(self.artistName,1)
    self.albumName = QLabel(self.songData["data"]["album"])
    self.albumName.setStyleSheet("color: grey; font-size:10px; font-weight:600")
    self.songInfoLayout.addWidget(self.albumName,1)
    self.mainLayout.addWidget(self.songInfoWidget, 1)
    ##

    # Add / Remove song button #
    self.buttonContainerWidget = QWidget()
    self.buttonContainerLayout = QVBoxLayout(self.buttonContainerWidget)
    self.buttonContainerLayout.setContentsMargins(0,0,0,0)
    self.button = QPushButton()
    self.button.setFixedSize(80,80)
    self.button.setCursor(Qt.CursorShape.PointingHandCursor)
    self.buttonContainerLayout.addWidget(self.button)
    self.mainLayout.addWidget(self.buttonContainerWidget)

    if self.songData["inplaylist"] == True:
      self.button.setText("Remove!")
      self.button.added = True
      self.button.setStyleSheet(f"background-color: {colors.color3}; border-radius:10px; font-size:13px; color: red; font-weight:700")
    else:
      self.button.setText("Add!")
      self.button.added = False
      self.button.setStyleSheet(f"background-color: {colors.color3}; border-radius:10px; font-size:15px; color: white; font-weight:700")
    
    self.button.clicked.connect(lambda: self.addOrRemoveSongFromPlaylist(self.songData))
    ##

    self.topLayout.addWidget(self.mainWidget)
  
  def addOrRemoveSongFromPlaylist(self, songData):
    addedStatus = self.button.added

    if addedStatus: # Song is already in the playlist
      print("Removing from playlist")
      self.cursor.execute("DELETE FROM playlists WHERE playlistName = ? AND location = ?", (self.songData["playlistName"], self.songData["data"]["location"]))
      self.button.added = False
      self.button.setStyleSheet(f"background-color: {self.colors.color3}; border-radius:10px; font-size:15px; color: white; font-weight:700")
      self.button.setText("Add!")
    else:
      print("Adding to playlist")
      self.cursor.execute("INSERT INTO playlists (playlistName, location) VALUES (?,?)", (self.songData["playlistName"], self.songData["data"]["location"]))
      self.button.added = True
      self.button.setStyleSheet(f"background-color: {self.colors.color3}; border-radius:10px; font-size:13px; color: red; font-weight:700")
      self.button.setText("Remove!")