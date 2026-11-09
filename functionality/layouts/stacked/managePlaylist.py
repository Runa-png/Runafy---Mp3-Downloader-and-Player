from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QLabel,
  QScrollArea,
  QHBoxLayout,
  QPushButton,
  QSizePolicy
)

from PyQt6.QtCore import Qt, pyqtSignal

from sqlite3 import connect, Row

from functionality.functions.searcher.extractArt import extractAlbumArt
from functionality.layouts.windows.playlistSettings import playlistSettingsWidget

class ManagePlaylistWidget(QWidget):
  UPDATE_LEFT_BAR = pyqtSignal()
  SET_STACKED_WIDGET = pyqtSignal(str)
  UPDATE_PLAYLIST = pyqtSignal()
  
  def __init__(self, colors):
    super().__init__()
    self.colors = colors

    self.manageWidget = QWidget()
    self.manageWidget.setStyleSheet(f"background-color: {colors.color3}")
    self.manageWidget.setContentsMargins(0,0,0,0)
    self.manageLayout = QVBoxLayout(self.manageWidget)
    self.manageLayout.setContentsMargins(0,0,0,0)

    self.scrollableArea = QScrollArea()
    self.scrollableArea.setWidgetResizable(True)
    self.scrollableWidget = QWidget()
    self.scrollableLayout = QVBoxLayout(self.scrollableWidget)
    self.scrollableLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.scrollableArea.setWidget(self.scrollableWidget)
    self.manageLayout.addWidget(self.scrollableArea)

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.manageWidget)

    # Variables
    self.presentWidgets = {}
  
  def showEvent(self, *args):
    print("Showing manage playlists")

    self.purgeWidgets()
    self.createPlaylistItems()

  def createPlaylistItems(self):
    connection = connect("database.db")
    cursor = connection.cursor()
    cursor.row_factory = Row

    uniquePlaylists = cursor.execute("SELECT DISTINCT playlistName FROM playlists").fetchall()
    uniquePlaylists = list(map(dict, uniquePlaylists))

    for playlist in uniquePlaylists:
      playlistData = cursor.execute("SELECT location FROM playlists WHERE playlistName = ?", (playlist["playlistName"],))

      newWidget = playlistItem(playlistData, self.colors, playlist["playlistName"])
      self.presentWidgets[playlist["playlistName"]] = newWidget

      newWidget.PLAYLIST_DELETED.connect(lambda name: self.playlistDeleted(name))
      newWidget.PLAYLIST_SELECTED.connect(lambda name: self.SET_STACKED_WIDGET.emit(name))
      newWidget.PLAYLIST_UPDATED.connect(lambda: self.UPDATE_PLAYLIST.emit())
      
      self.scrollableLayout.addWidget(newWidget)
    
    connection.close()

  def purgeWidgets(self):
    for key in self.presentWidgets:
      self.presentWidgets[key].hide()
  
  def playlistDeleted(self, name):
    self.presentWidgets[name].hide()
    self.presentWidgets.pop(name)
    self.UPDATE_LEFT_BAR.emit()

class playlistItem(QWidget):
  PLAYLIST_DELETED = pyqtSignal(str)
  PLAYLIST_SELECTED = pyqtSignal(str)
  PLAYLIST_UPDATED = pyqtSignal()
  def __init__(self, songData, colors, playlistName):
    super().__init__()
    self.setCursor(Qt.CursorShape.PointingHandCursor)

    self.mainLayout = QVBoxLayout(self)
    self.colors = colors
    self.playlistNameVariable = playlistName

    data = songData.fetchall()
    length = len(data)
    playlistData = data[0]

    self.topWidget = QWidget()
    self.topWidget.setFixedHeight(100)
    self.topWidget.setStyleSheet(f"background-color: {colors.color2}; border-radius:10px")

    self.topLayout = QHBoxLayout(self.topWidget)

    self.albumImage = QLabel()
    albumImage = extractAlbumArt(self, playlistData["location"], 20)
    albumImageScaled = albumImage.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.albumImage.setPixmap(albumImageScaled)

    self.informationWidget = QWidget()
    self.informationWidget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred) # Crushes text horizontally, does nothing vertically (fixed height)    
    self.informationLayout = QVBoxLayout(self.informationWidget)
    self.informationLayout.setContentsMargins(0,0,0,0)
    self.informationLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    self.playlistName = QLabel(playlistName)
    self.playlistName.setStyleSheet(f"color: {self.colors.text1}; font-size:25px; font-weight:800")
    self.playlistLength = QLabel(str(length)+ " Songs")
    self.playlistLength.setStyleSheet(f"color: {self.colors.text2}; font-size:20px; font-weight:800")
    
    self.informationLayout.addWidget(self.playlistName)
    self.informationLayout.addWidget(self.playlistLength)

    self.buttonWidget = QWidget()
    self.buttonLayout = QHBoxLayout(self.buttonWidget)
    self.buttonLayout.setContentsMargins(0,0,0,0)
    
    self.addButton = QPushButton("Manage \n Songs")
    self.addButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.addButton.setStyleSheet(f"background-color:{colors.color3}; border-radius:10px; font-size:16px; font-weight:700; color: {self.colors.text1}")
    self.addButton.setFixedSize(80,80)
    self.addButton.clicked.connect(lambda _, playlistName=playlistName: self.showPlaylistSettings(playlistName))
    self.buttonLayout.addWidget(self.addButton)
    
    self.deleteButton = QPushButton("Delete")
    self.deleteButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.deleteButton.setStyleSheet(f"background-color:{colors.color3}; border-radius:10px; font-size:15px; font-weight:700; color: {self.colors.text1}")
    self.deleteButton.setFixedSize(80,80)
    self.deleteButton.deletePressed = False # Set to true when pressed, then delete if pressed again
    self.deleteButton.clicked.connect(lambda _, playlistName=playlistName: self.deleteButtonPressed(playlistName))
    self.buttonLayout.addWidget(self.deleteButton)

    self.topLayout.addWidget(self.albumImage)
    self.topLayout.addWidget(self.informationWidget, 1)
    self.topLayout.addWidget(self.buttonWidget)

    self.mainLayout.addWidget(self.topWidget)
  
  def deleteButtonPressed(self, playlistName):
    status = self.deleteButton.deletePressed

    if not status: # First press of delete button
      self.deleteButton.setText("Are \n you \n sure?")
      self.deleteButton.setStyleSheet(f"color: {self.colors.failed_fetch}; font-size:15px; font-weight:700; background-color: {self.colors.color3}")
      self.deleteButton.deletePressed = True
      return
    
    # Second press of delete, user has made no mistake surprisingly
    connection = connect("database.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM playlists WHERE playlistName = ?", (playlistName,))

    connection.commit()
    connection.close()

    self.PLAYLIST_DELETED.emit(playlistName)
  
  def showPlaylistSettings(self, playlistName):
    print("Showing playlist settings window")
    self.settingsWidget = playlistSettingsWidget(playlistName)
    self.settingsWidget.PLAYLIST_UPDATED.connect(lambda: self.PLAYLIST_UPDATED.emit())
    self.settingsWidget.show()

  def mousePressEvent(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      self.PLAYLIST_SELECTED.emit(self.playlistNameVariable)