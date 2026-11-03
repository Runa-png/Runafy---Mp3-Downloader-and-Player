from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QScrollArea,
  QPushButton,
  QLineEdit,
  QComboBox,
  QListView,
  QSizePolicy
)

from PyQt6.QtCore import (
  Qt,
  pyqtSignal
)

import sqlite3

from functionality.functions.searcher.extractArt import extractAlbumArt
from functionality.functions.searcher.getFileData import getFileData
from functionality.functions.playlists.sortByName import sortPlaylist

class CreateWidget(QWidget):
  PLAYLIST_CREATED = pyqtSignal()
  
  def __init__(self, colors):
    super().__init__()

    self.colors = colors

    self.createWidget = QWidget()
    self.createWidget.setStyleSheet(f"background-color: {colors.color3}")
    self.createColumn = QVBoxLayout(self.createWidget)

    userInputWidth = 130 # Used for dropdown and search button
    
    # User inputs #
    self.mainContainerWidget = QWidget()
    self.mainContainerWidget.setFixedHeight(75)
    self.mainContainerLayout = QVBoxLayout(self.mainContainerWidget)
    self.mainContainerLayout.setContentsMargins(0,0,0,0)
    
    self.playlistNameInput = QLineEdit()
    self.playlistNameInput.setPlaceholderText("Playlist Name")
    self.playlistNameInput.setStyleSheet(f"border: 2px solid {self.colors.custom_color_1}; border-radius:10px; padding: 3px; color:white; font-size: 15px; background-color: {colors.color1}")

    self.playlistNameButton = QPushButton("Create!")
    self.playlistNameButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.playlistNameButton.setFixedHeight(30)
    self.playlistNameButton.setFixedWidth(userInputWidth)
    self.playlistNameButton.setStyleSheet(f"background-color: {colors.custom_color_1}; color: white; font-size:13px; font-weight:800; border:2px solid {self.colors.color2}; padding:6px; border-radius: 5px")

    # Create playlist connection
    self.playlistNameButton.clicked.connect(lambda: self.createPlaylist())

    self.searchBar = QLineEdit()
    self.searchBar.selectedOption = "Song Name"
    self.searchBar.setPlaceholderText(f"Search By Name")
    self.searchBar.setStyleSheet(f"border: 2px solid {self.colors.custom_color_1}; border-radius:10px; padding: 3px; color:white; font-size: 15px; background-color: {colors.color1}")

    self.searchBar.editingFinished.connect(lambda: self.reload())

    ## Playlist name layout ##
    self.playlistNameWidget = QWidget()
    self.playlistNameLayout = QHBoxLayout(self.playlistNameWidget)
    self.playlistNameLayout.setContentsMargins(0,0,0,0)

    self.playlistNameLayout.addWidget(self.playlistNameInput)
    self.playlistNameLayout.addWidget(self.playlistNameButton)
    ##

    ## Song search layout ##
    self.songSearchWidget = QWidget()
    self.songSearchLayout = QHBoxLayout(self.songSearchWidget)
    self.songSearchLayout.setContentsMargins(0,0,0,0)

    self.songSearchLayout.addWidget(self.searchBar)

    self.searchOptionDropdown = QComboBox()
    self.searchOptionDropdown.setFixedWidth(userInputWidth)
    self.searchOptionDropdown.setFixedHeight(30)
    self.searchOptionDropdown.setStyleSheet(f"""
      QComboBox {{
      color: white;
      font-size: 13px;
      font-weight: 800;
      border: 2px solid {colors.color2};
      padding-left: 3px;
      background-color: {colors.custom_color_1};
      border-radius:5px;
      }}

      QComboBox QAbstractItemView {{
        border:2px solid {colors.color1}
      }}
    """)
    self.searchOptionDropdown.addItem("Song Name")
    self.searchOptionDropdown.addItem("Artist Name")
    self.searchOptionDropdown.addItem("Album Name")

    def dropdownUpdated(self):
      self.searchBar.setText("") # QOL remove text so the filter takes priority
      self.reload() # Reload to apply filter

    self.searchOptionDropdown.currentTextChanged.connect(lambda: dropdownUpdated(self))

    self.songSearchLayout.addWidget(self.searchOptionDropdown)
    ##

    self.mainContainerLayout.addWidget(self.playlistNameWidget)
    self.mainContainerLayout.addWidget(self.songSearchWidget)

    self.createColumn.addWidget(self.mainContainerWidget)

    # Scrollable Area #
    self.scrollableArea = QScrollArea()
    self.scrollableArea.setStyleSheet(f"border: none; background-color:{self.colors.color3}")
    self.scrollableArea.setWidgetResizable(True)
    self.scrollableAreaWidget = QWidget()
    self.scrollableAreaLayout = QVBoxLayout(self.scrollableAreaWidget)
    self.scrollableAreaLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.scrollableAreaLayout.setSpacing(5)
    self.scrollableArea.setWidget(self.scrollableAreaWidget)
    
    self.createColumn.addWidget(self.scrollableArea)
    ##

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.createWidget)

    # Variables 
    self.scrollableWidgets = {}
    self.selectedSongs = {}

  
  def showEvent(self, _): # Runs when the widget is shown
    self.reload()
  
  def findSongs(self):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    songs = cursor.execute("SELECT * FROM songs")

    self.songData = []
    count = 0
    for song in songs:
      # Format the data
      tempSongData = {"name": song[0], "artist": song[1], "album": song[2], "location": song[3], "index": count}
      self.songData.append(tempSongData)
      count += 1
    
    connection.close()

    self.sortOption()

    for songData in self.songData:
      newWidget = SongWidget(songData, self.colors, self.selectedSongs)
      self.scrollableWidgets[songData["index"]] = newWidget
      self.scrollableAreaLayout.addWidget(newWidget)
  
  def purgeScrollableWidgets(self):
    self.songData = []
    self.selectedSongs = {}

    for key in self.scrollableWidgets:
      self.scrollableWidgets[key].hide()

  def createPlaylist(self):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    
    playlistName = self.playlistNameInput.text()

    if not playlistName.strip():
      print("No playlist name input")
      playlistName = self.playlistNameInput.setText("You need to input a playlist name")
      return
    
    if not self.selectedSongs:
      print("No songs chosen")
      playlistName = self.playlistNameInput.setText("No songs chosen")
      return


    exists = cursor.execute("SELECT * FROM playlists WHERE playlistName = ?", (playlistName,)).fetchall()
    if exists:
      print("Playlist name exists")
      playlistName = self.playlistNameInput.setText("Playlist name already in use")
      return
    
    for key in self.selectedSongs:
      song = self.selectedSongs[key]

      cursor.execute("INSERT INTO playlists (playlistName, location) VALUES (?,?)", (playlistName, song["location"]))
    
    connection.commit()
    connection.close()

    self.reload()
    playlistName = self.playlistNameInput.setText("Success!")
    self.PLAYLIST_CREATED.emit()
  
  def reload(self):
    self.purgeScrollableWidgets()
    self.findSongs()

  def sortOption(self):
    text = self.searchBar.text()
    if text:
      sortPlaylist(self.songData, text)
      return # Prevent search by option
    
    option = (self.searchOptionDropdown.currentText())
    if option == "Song Name":
      print("Sorting by name")
      self.songData.sort(key=lambda song: song["name"].lower())
    elif option == "Artist Name":
      print("Sorting by artist name")
      self.songData.sort(key=lambda song: song["artist"].lower())
    else:
      print("Sorting by album name")
      self.songData.sort(key=lambda song: song["album"].lower())


class SongWidget(QWidget):
  UPDATE_BUTTON = pyqtSignal()
  
  def addButtonPressed(self, songData, selectedSongsPointer):
    try:
      selectedSongsPointer[songData["index"]]
      selectedSongsPointer.pop(songData["index"])
      print("Song Removed")

      self.addButton.setStyleSheet(f"background-color: {self.colors.custom_color_1}; color: white; font-size:20px; font-weight:800")
      
      self.addButton.setText("Add!")
    except:
      selectedSongsPointer[songData["index"]] = songData

      self.addButton.setStyleSheet(f"background-color: {self.colors.custom_color_1}; color: rgb(184, 0, 0); font-size:15px; font-weight:800")

      print("Song added")

      self.addButton.setText("Remove!")
  
  def __init__(self, data, colors, selectedSongsPointer):
    super().__init__()

    height = 80
    self.colors = colors

    topLayout = QVBoxLayout(self)
    topLayout.setContentsMargins(0,0,0,0)

    mainWidget = QWidget()
    mainWidget.setStyleSheet(f"background-color: {colors.color2}; border-radius: 15px")

    mainLayout = QHBoxLayout(mainWidget)
    mainLayout.setContentsMargins(10,10,10,10)

    # Album Image
    albumArtWidget = QWidget()
    albumArtWidget.setFixedWidth(height)
    albumArtLayout = QHBoxLayout(albumArtWidget)
    albumArtLayout.setContentsMargins(0,0,0,0)
    
    albumArt = extractAlbumArt(self, data["location"], 40)
    albumLabel = QLabel()
    if albumArt != None:
      albumLabel.setPixmap(albumArt.scaled(height,height,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
    
    albumArtLayout.addWidget(albumLabel)
    mainLayout.addWidget(albumArtWidget)
    ##

    # Text Widgets #
    nameLabel = QLabel(data["name"])
    nameLabel.setStyleSheet("font-size: 21px; font-weight: 700; color: rgb(255,255,255)")
    artistLabel = QLabel(data["artist"])
    artistLabel.setStyleSheet("font-size: 15px; font-weight: 700; color: rgb(199, 199, 199)")
    albumLabel = QLabel(data["album"])
    albumLabel.setStyleSheet("font-size: 14px; font-weight: 700; color: rgb(125, 125, 125)")

    dataContainerWidget = QWidget()
    dataContainerWidget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred) # Crushes text horizontally, does nothing vertically (fixed height)
    dataContainerLayout = QVBoxLayout(dataContainerWidget)
    dataContainerLayout.setContentsMargins(0,0,0,0)
    dataContainerLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

    dataContainerLayout.addWidget(nameLabel)
    dataContainerLayout.addWidget(artistLabel)
    dataContainerLayout.addWidget(albumLabel)

    mainLayout.addWidget(dataContainerWidget, 1)
    ##

    # Add button #
    buttonWidget = QWidget()
    buttonLayout = QVBoxLayout(buttonWidget)
    buttonLayout.setContentsMargins(0,0,0,0)

    self.addButton = QPushButton("Add!")
    self.addButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.addButton.setFixedSize(height,height)
    self.addButton.setStyleSheet(f"background-color: {colors.custom_color_1}; color: white; font-size:20px; font-weight:800")

    buttonLayout.addWidget(self.addButton)
    mainLayout.addWidget(buttonWidget)
    ##

    self.addButton.clicked.connect(lambda: self.addButtonPressed(data, selectedSongsPointer))

    topLayout.addWidget(mainWidget)
