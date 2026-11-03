from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QLineEdit,
  QPushButton,
  QComboBox,
  QProgressBar,
  QScrollArea,
  QSizePolicy
)

from PyQt6.QtCore import (
  Qt,
  QThreadPool,
  pyqtSignal
)

from functionality.functions.download.fetchYoutubeUrl import findYoutubeUrl
from functionality.workers.searchingWorker import fetchFileWorker
from functionality.workers.downloadingWorker import downloadFileWorker

import sqlite3
import shutil

class DownloadWidget(QWidget):
  def __init__(self, colors):
    super().__init__()
    self.colors = colors

    self.downloadWidget = QWidget()
    self.downloadWidget.setStyleSheet(f"background-color: {colors.color3}")
    self.downloadWidget.setContentsMargins(0,0,0,0)
    self.downloadColumn = QVBoxLayout(self.downloadWidget)
    self.downloadColumn.setContentsMargins(0,0,0,0)

    # Align Top #
    self.alignTopWidget = QWidget()
    self.alignTopWidget.setFixedHeight(85)
    self.alignTopLayout = QVBoxLayout(self.alignTopWidget)
    self.downloadColumn.addWidget(self.alignTopWidget, alignment=Qt.AlignmentFlag.AlignTop)
    ##

    # User input bar
    self.inputWidget = QWidget()
    self.inputLayout = QHBoxLayout(self.inputWidget)
    self.inputLayout.setContentsMargins(0,0,0,0)
    
    self.textInput = QLineEdit()
    self.textInput.setStyleSheet(f"color: {colors.color4}; font-size: 15px")
    self.textInput.setPlaceholderText("CSV Location")
    self.textInput.setFixedHeight(30)

    self.downloadButton = QPushButton("Download")
    self.downloadButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.downloadButton.setStyleSheet(f"color: {colors.color4}; font-size: 15px; border:none; background-color:{colors.color2}; border-radius:10px; font-weight:800")
    self.downloadButton.setFixedSize(90,30)

    self.searchButton = QPushButton("Search")
    self.searchButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.searchButton.setStyleSheet(f"color: {colors.color4}; font-size: 15px; border:none; background-color:{colors.color2}; border-radius:10px; font-weight:800")
    self.searchButton.setFixedSize(90,30)

    self.inputLayout.addWidget(self.textInput, stretch=1)
    self.inputLayout.addWidget(self.searchButton)
    self.inputLayout.addWidget(self.downloadButton)

    self.alignTopLayout.addWidget(self.inputWidget, stretch=1, alignment=Qt.AlignmentFlag.AlignTop)
    ##

    # Status Bar
    self.statusBarWidget = QWidget()
    self.statusBarWidget.setContentsMargins(0,0,0,0)
    self.statusBarLayout = QHBoxLayout(self.statusBarWidget)
    self.statusBarLayout.setContentsMargins(0,0,0,0)
    self.statusBar = QProgressBar()
    self.statusBar.setFixedHeight(25)
    ##

    # Scrollable Area
    self.scrollableArea = QScrollArea()
    self.scrollableArea.setWidgetResizable(True)
    self.scrollableArea.setStyleSheet("border: none")
    
    self.scrollableAreaWidget = QWidget()
    self.scrollableAreaLayout = QVBoxLayout(self.scrollableAreaWidget)
    self.scrollableAreaLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.scrollableAreaLayout.setSpacing(20)

    self.scrollableArea.setWidget(self.scrollableAreaWidget)
    self.downloadColumn.addWidget(self.scrollableArea)
    ##

    self.statusBar.setStyleSheet(f"""
      QProgressBar {{
        background-color: {colors.color2};
        border: 1px solid {colors.color2};
        border-radius: 10px;
        text-align: center;
        color: {colors.color4}
      }}

      QProgressBar::chunk {{
        background-color: #e0b745;
        border-radius: 10px;
      }}
    """)

    self.statusBarLayout.addWidget(self.statusBar)
    self.alignTopLayout.addWidget(self.statusBarWidget, stretch=1)
    ##

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.downloadWidget, stretch=1)

    self.searchButton.clicked.connect(lambda: self.searchButtonPressed(self.textInput.text()))
    self.downloadButton.clicked.connect(lambda: self.downloadButtonPressed())

    # Variables
    self.searchedCSV = None # Trust me this will save a lot of headache if i need it
    self.songWidgets = {}
  
    # Multithreading
    self.threadPool = QThreadPool()
    self.worker = None
    self.appClosed = False
    self.running = False

  def searchButtonPressed(self, location):
    def searchSongs(self, location):
      self.purgeSearchedSongs()
      
      self.worker = fetchFileWorker(location)

      self.worker.signals.URL_FOUND.connect(lambda songData: self.addSong(songData))
      self.worker.signals.COUNT.connect(lambda count: self.statusBar.setValue(count))
      self.worker.signals.FINISHED.connect(lambda: setattr(self, "running", False))
      self.worker.signals.STATUS.connect(lambda status: self.textInput.setText(status))

      self.running = True
      self.threadPool.start(self.worker)
    
    if not self.running:
      if not location:
        self.textInput.setText("Invalid file location")
        return

      searchSongs(self, location)
  
  def downloadButtonPressed(self):
    def moveFromCache(self):
      self.running = False

      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()

      for index in self.songWidgets:
        data = self.songWidgets[index]
        
        try:
          downloadData = data["downloadData"]
          destination = "music/" + downloadData["fileName"]
          songData = data["data"]
          cursor.execute("INSERT INTO songs (name, artist, album, location) VALUES (?,?,?,?)", (songData["name"], songData["artist"], songData["album"], destination))
          shutil.move(downloadData["fileLocation"], destination)
        except TypeError: # Happens when the song is already in the database
          print("Song already in database")
          continue
        except KeyError: # Happens when the download fails
          print("Download didn't complete")
          continue
      
      connection.commit()
      connection.close()

    if not self.running:
      self.statusBar.setValue(0)
      self.worker = downloadFileWorker(self.songWidgets)

      self.worker.signals.FINISHED.connect(lambda: moveFromCache(self))
      self.worker.signals.COUNT.connect(lambda count: self.statusBar.setValue(count))

      self.running = True
      self.threadPool.start(self.worker)
  
  def killWorker(self):
    if self.worker:
      self.worker.running = False
    
  def addSong(self, songData): # to the scrollable area
    newWidget = NewSongWidget(self.colors, songData)
    newWidget.BUTTON_PRESSED.connect(lambda data: self.optionPressed(data))
    self.songWidgets[songData["index"]] = {"index": songData["index"], "widget": newWidget, "data": songData}

    self.scrollableAreaLayout.addWidget(newWidget)
  
  def purgeSearchedSongs(self):
    for key in self.songWidgets:
      self.songWidgets[key]["widget"].hide()
    
    self.songWidgets.clear()
  
  def optionPressed(self, optionData):
    if optionData["command"] == "SETTINGS":
      self.settingsWindow = SettingsWindow(optionData["index"], self.songWidgets, self.colors)
      self.settingsWindow.show()

      self.settingsWindow.CHANGE_URL.connect(lambda newData: self.updateUrl(newData))
    elif optionData["command"] == "REMOVE":
      index = optionData["index"]
      self.songWidgets[index]["widget"].hide()
      self.songWidgets.pop(index)
  
  def updateUrl(self, updateData):
    self.songWidgets[updateData["index"]]["data"]["url"] = updateData["newUrl"]
    self.songWidgets[updateData["index"]]["data"]["id"] = None

class NewSongWidget(QWidget):
  BUTTON_PRESSED = pyqtSignal(dict)
  
  def __init__(self, colors, songData):
    super().__init__()
    height = 100

    topLayout = QVBoxLayout(self)

    mainWidget = QWidget()
    mainWidget.setFixedHeight(height)
    mainWidget.setStyleSheet(f"background-color: {colors.color2}; border-radius:10px")
    
    mainLayout = QHBoxLayout(mainWidget)
    mainLayout.setContentsMargins(20,10,20,10)

    # Song name #
    songWidget = QScrollArea()
    songWidget.setStyleSheet("border: none")
    songLayout = QVBoxLayout(songWidget)

    self.songName = QLabel(songData["name"])
    self.songName.setStyleSheet("color: white; font-size:18px; font-weight:600")
    songLayout.addWidget(self.songName, alignment = Qt.AlignmentFlag.AlignCenter)
    ##

    # Fetched artist name #
    artistWidget = QScrollArea()
    artistWidget.setStyleSheet("border: none")
    artistLayout = QVBoxLayout(artistWidget)

    artistName = QLabel(songData["uploader"])
    artistName.setStyleSheet("color: white; font-size:14px; font-weight:600")
    artistLayout.addWidget(artistName, alignment = Qt.AlignmentFlag.AlignCenter)
    ##

    # Accuracy #
    accuracyWidget = QScrollArea()
    accuracyWidget.setStyleSheet("border: none")
    accuracyLayout = QVBoxLayout(accuracyWidget)

    accuracyLabel = QLabel(f"{songData["ratio"]}% Accurate")
    accuracyLabel.setStyleSheet("color: white; font-size:15px; font-weight:800")
    accuracyLayout.addWidget(accuracyLabel, alignment = Qt.AlignmentFlag.AlignCenter)
    ##

    # Settings Button #
    settingsButtonWidget = QWidget()
    settingsButtonLayout = QVBoxLayout(settingsButtonWidget)
    settingsButtonLayout.setContentsMargins(0,0,0,0)

    settingsButton = QPushButton("Settings")
    settingsButton.setCursor(Qt.CursorShape.PointingHandCursor)
    settingsButton.setSizePolicy(
      QSizePolicy.Policy.Expanding,
      QSizePolicy.Policy.Fixed
    )
    settingsButton.setStyleSheet(f"color: white; font-size:20px; font-weight:800; border: none; background-color: {colors.custom_color_1}; padding:10px; border-radius:10px")
    settingsButton.setFixedHeight(height-20)
    settingsButtonLayout.addWidget(settingsButton)

    settingsButton.clicked.connect(lambda _, index=songData["index"]: self.BUTTON_PRESSED.emit({"index": index, "command": "SETTINGS"}))
    ##

    # Remove Button #
    removeButtonWidget = QWidget()
    removeButtonLayout = QVBoxLayout(removeButtonWidget)
    removeButtonLayout.setContentsMargins(0,0,0,0)

    removeButton = QPushButton("Remove")
    removeButton.setCursor(Qt.CursorShape.PointingHandCursor)
    removeButton.setSizePolicy(
      QSizePolicy.Policy.Expanding,
      QSizePolicy.Policy.Fixed
    )
    removeButton.setStyleSheet(f"color: white; font-size:20px; font-weight:800; border: none; background-color: {colors.custom_color_1}; padding:10px; border-radius:10px")
    removeButton.setFixedHeight(height-20)
    removeButtonLayout.addWidget(removeButton)

    removeButton.clicked.connect(lambda _, index=songData["index"]: self.BUTTON_PRESSED.emit({"index": index, "command": "REMOVE"}))
    ##

    mainLayout.addWidget(songWidget, 3)
    mainLayout.addWidget(artistWidget, 4)
    mainLayout.addWidget(accuracyWidget, 2)
    mainLayout.addWidget(settingsButtonWidget, 1)
    mainLayout.addWidget(removeButtonWidget, 1)

    topLayout.addWidget(mainWidget, alignment = Qt.AlignmentFlag.AlignTop)
  
class SettingsWindow(QWidget):
  CHANGE_URL = pyqtSignal(dict)
  
  def __init__(self, index, widgets, colors):
    super().__init__()

    self.setFixedSize(600,600)

    topLayout = QVBoxLayout(self)
    topLayout.setContentsMargins(0,0,0,0)

    mainWidget = QWidget()
    mainWidget.setContentsMargins(0,0,0,0)
    mainWidget.setStyleSheet(f"background-color: {colors.color3}")

    mainLayout = QVBoxLayout(mainWidget)
    mainLayout.setContentsMargins(0,0,0,0)

    data = widgets[index]["data"]

    # Title #
    titleWidget = QWidget()
    titleWidget.setFixedHeight(80)
    titleLayout = QHBoxLayout(titleWidget)
    titleLayout.setContentsMargins(0,20,0,20)
    
    title = QLabel("Change Song URL")
    title.setStyleSheet("color: white; font-size: 25px; text-decoration: underline; font-weight: 800")

    titleLayout.addWidget(title, alignment = Qt.AlignmentFlag.AlignCenter)
    mainLayout.addWidget(titleWidget)
    
    # Name #
    name = QLabel(data["name"])
    name.setStyleSheet("font-size: 18px; font-weight: 800; color: white")

    # Artist #
    artist = QLabel(data["artist"])
    artist.setStyleSheet("font-size: 14px; font-weight: 800; color: darkgray")

    # Album #
    album = QLabel(data["album"])
    album.setStyleSheet("font-size: 12px; font-weight: 800; color: dimgray")

    # Collect all the information widgets together #
    infoCollectedWidget = QWidget()
    infoCollectedLayout = QVBoxLayout(infoCollectedWidget)
    infoCollectedLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    infoCollectedLayout.setSpacing(50)

    infoCollectedLayout.addWidget(name, alignment=Qt.AlignmentFlag.AlignCenter)
    infoCollectedLayout.addWidget(artist, alignment=Qt.AlignmentFlag.AlignCenter)
    infoCollectedLayout.addWidget(album, alignment=Qt.AlignmentFlag.AlignCenter)

    # Inputs
    urlEdit = QLineEdit()
    urlEdit.setStyleSheet(f"border: 2px solid {colors.custom_color_1}; padding: 3px; color:white; font-size: 15px; background-color: {colors.color1}")
    urlEdit.setText(str(data["url"]))

    # Update Button
    updateButton = QPushButton("Update!")
    updateButton.setCursor(Qt.CursorShape.PointingHandCursor)
    updateButton.setStyleSheet(f"border: 2px solid {colors.custom_color_1}; padding: 3px; color:white; font-size: 25px; background-color: {colors.color1}; font-weight:900")

    # Collect all the inputs #
    inputsWidget = QWidget()
    inputsWidget.setFixedHeight(200)
    inputsLayout = QVBoxLayout(inputsWidget)

    inputsLayout.addWidget(urlEdit)
    inputsLayout.addWidget(updateButton)

    # Collect all the internal widgets
    contentsPaddingLayout = QVBoxLayout()
    contentsPaddingLayout.setContentsMargins(20,20,20,20)
    
    internalWidget = QWidget()
    internalWidget.setStyleSheet(f"background-color: {colors.color2}; border-radius: 10px")
    internalLayout = QVBoxLayout(internalWidget)

    internalLayout.addWidget(infoCollectedWidget)
    internalLayout.addWidget(inputsWidget)

    contentsPaddingLayout.addWidget(internalWidget)
    
    mainLayout.addLayout(contentsPaddingLayout)

    topLayout.addWidget(mainWidget)

    # Give functionality to the update button
    updateButton.clicked.connect(lambda: self.CHANGE_URL.emit({"index": index, "newUrl": urlEdit.text()}))

