from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QLabel,
  QHBoxLayout,
  QPushButton,
  QScrollArea,
  QSizePolicy
)

from PyQt6.QtCore import Qt, pyqtSignal

import sqlite3
import os

from functionality.functions.searcher.extractArt import extractAlbumArt

class ManageMusicWidget(QWidget):
  SONG_DELETED = pyqtSignal()
  
  def __init__(self, colors):
    super().__init__()
    self.colors = colors

    self.manageWidget = QWidget()
    self.manageWidget.setStyleSheet(f"background-color: {colors.color3}")
    self.manageWidget.setContentsMargins(0,0,0,0)
    
    self.manageColumn = QVBoxLayout(self.manageWidget)
    self.manageColumn.setContentsMargins(0,0,0,0)

    self.scrollableArea = QScrollArea()
    self.scrollableArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) # Disable horizontal scrolling
    self.scrollableArea.setWidgetResizable(True)
    
    self.scrollableWidget = QWidget()
    self.scrollableLayout = QVBoxLayout(self.scrollableWidget)
    self.scrollableLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.scrollableArea.setWidget(self.scrollableWidget)
    self.manageColumn.addWidget(self.scrollableArea)

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.manageWidget)

    # Variables
    self.presentWidgets = {}
  
  def purgeWidgets(self):
    for index in self.presentWidgets:
      self.presentWidgets[index].hide()
  
  def showEvent(self, *args):
    self.purgeWidgets()
    self.findMusic()
  
  def findMusic(self):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row

    self.songs = cursor.execute("SELECT * FROM songs").fetchall()
    self.songs.sort(key=lambda song: song["name"])

    index = 0
    for song in self.songs:
      songDict = dict(song)

      self.widget = songItem(songData=songDict, colors=self.colors, index=index)
      self.presentWidgets[index] = self.widget
      self.scrollableLayout.addWidget(self.widget)

      self.widget.DELETE_SONG.connect(lambda index: self.deleteSong(index=index))

      index += 1
  
  def deleteSong(self, index):
    songData = (self.presentWidgets[index].songData)

    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON") # If we delete something then we need all entries removed
    cursor = connection.cursor()

    cursor.execute("DELETE FROM songs WHERE location = ?", (songData["location"],))
    os.remove(songData["location"])
    connection.commit()
    connection.close()

    self.presentWidgets[index].hide()
    self.presentWidgets.pop(index)

    self.SONG_DELETED.emit()

class songItem(QWidget):
  DELETE_SONG = pyqtSignal(int)
  
  def __init__(self, songData, colors, index):
    super().__init__()
    self.songData = songData
    self.colors = colors
    self.index = index

    self.setFixedHeight(120)

    self.topLayout = QVBoxLayout(self)

    self.mainWidget = QWidget()
    self.mainWidget.setStyleSheet(f"background-color: {self.colors.color2}; border-radius: 10px")
    self.mainLayout = QHBoxLayout(self.mainWidget)

    # Song Image
    self.albumImage = QLabel()
    self.albumImage.setPixmap(extractAlbumArt(self, self.songData["location"], 20).scaled(75,75,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
    self.mainLayout.addWidget(self.albumImage)
    ##

    # Song Information
    self.informationWidget = QWidget()
    self.informationWidget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred) # Crushes text horizontally, does nothing vertically (fixed height)
    self.informationLayout = QHBoxLayout(self.informationWidget)
    self.informationLayout.setSpacing(30)

    self.name = QLabel(self.songData["name"])
    self.name.setStyleSheet("color:white; font-weight:700; font-size:18px")
    self.artist = QLabel(self.songData["artist"])
    self.artist.setStyleSheet("color:darkgray; font-weight:700; font-size:15px")
    self.album = QLabel(self.songData["album"])
    self.album.setStyleSheet("color:gray; font-weight:700; font-size:12px")

    self.informationLayout.addWidget(self.name)
    self.informationLayout.addWidget(self.artist)
    self.informationLayout.addWidget(self.album)
    self.mainLayout.addWidget(self.informationWidget, 1)
    ##

    # Delete Button
    self.deleteButton = QPushButton("Delete")
    self.deleteButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.deleteButton.setFixedSize(80,80)
    self.deleteButton.setStyleSheet(f"border: none; border-radius:10px; background-color: {colors.custom_color_1}; color: white; font-size:17px; font-weight:800")
    self.mainLayout.addWidget(self.deleteButton)

    self.deleteButton.clicked.connect(lambda: self.DELETE_SONG.emit(self.index))
    ##

    self.topLayout.addWidget(self.mainWidget)
    