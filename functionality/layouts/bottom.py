from PyQt6.QtWidgets import (
  QWidget,
  QHBoxLayout,
  QVBoxLayout,
  QLabel,
  QPushButton,
  QSizePolicy,
  QSlider
)

from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QFontMetrics, QTransform, QIcon

import os
from random import shuffle
from copy import copy

from functionality.functions.searcher.extractArt import extractAlbumArt

from functionality.functions.draw.playButton import drawPlayPixmap
from functionality.functions.draw.forward import drawForwardPixmap
from functionality.functions.draw.pauseButton import drawPausePixmap
from functionality.functions.draw.shufflePixmap import drawShufflePixmap
from functionality.functions.draw.reloadPixmap import drawReloadPixmap

class BottomSection(QWidget):
  def __init__(self, colors):
    super().__init__()
    self.colors = colors

    # Player stuff
    self.player = QMediaPlayer()
    self.audioOutput = QAudioOutput()
    self.player.setAudioOutput(self.audioOutput)

    self.player.mediaStatusChanged.connect(lambda status: self.mediaChanged(status=status))

    self.playlist = []
    self.playerIndex = 0
    ##

    self.bottomWidget = QWidget()
    self.bottomWidget.setStyleSheet(f"background-color: {colors.color1}")
    self.bottomWidget.setFixedHeight(100)
    self.bottomLayout = QHBoxLayout(self.bottomWidget)
    self.bottomLayout.setContentsMargins(10,0,0,0)
    self.bottomLayout.setSpacing(0)

    # Left
    self.leftWidget = QWidget()
    self.leftLayout = QHBoxLayout(self.leftWidget)
    self.leftLayout.setContentsMargins(0,0,0,0)

    self.albumImage = QLabel()
    self.leftLayout.addWidget(self.albumImage)

    self.songInformationWidget = QWidget()
    self.songInformationLayout = QVBoxLayout(self.songInformationWidget)
    self.songInformationLayout.setContentsMargins(0,0,0,10)
    self.songInformationLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
    self.songName = QLabel()
    self.songName.setStyleSheet("color: white; font-size:15px; font-weight: 700")
    self.artistName = QLabel()
    self.artistName.setStyleSheet("color: darkgray; font-size:13px; font-weight: 700")
    self.albumName = QLabel()
    self.albumName.setStyleSheet("color: gray; font-size:11px; font-weight: 700")
    self.songInformationLayout.addWidget(self.songName)
    self.songInformationLayout.addWidget(self.artistName)
    self.songInformationLayout.addWidget(self.albumName)
    self.leftLayout.addWidget(self.songInformationWidget, 1)

    self.bottomLayout.addWidget(self.leftWidget, 1)
    
    # Middle
    self.middleWidget = QWidget()
    self.middleWidget.setMinimumWidth(280)

    self.middleLayout = QHBoxLayout(self.middleWidget)
    self.middleLayout.setContentsMargins(0,0,0,0)
    self.middleLayout.setSpacing(0)

    nextPixmap = drawForwardPixmap()

    previousPixmap = nextPixmap.transformed(QTransform().scale(-1, 1))
    previousScaledPixmap = previousPixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    self.previousIcon = QIcon(previousScaledPixmap)

    playPixmap = drawPlayPixmap()
    playScaledPixmap = playPixmap.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.playIcon = QIcon(playScaledPixmap)

    pausePixmap = drawPausePixmap()
    pauseScaledPixmap = pausePixmap.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.pauseIcon = QIcon(pauseScaledPixmap)

    nextScaledPixmap = nextPixmap.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.nextIcon = QIcon(nextScaledPixmap)
    
    self.previousLayout = QVBoxLayout()
    self.previousLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.previousLayout.setContentsMargins(0,0,0,0)
    self.previousButton = QPushButton()
    self.previousButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.previousButton.setIcon(self.previousIcon)
    self.previousButton.setIconSize(QSize(80,80))
    self.previousButton.setStyleSheet("border: none")
    self.previousLayout.addWidget(self.previousButton)
    
    self.playLayout = QVBoxLayout()
    self.playLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.playLayout.setContentsMargins(0,0,0,0)
    self.playButton = QPushButton()
    self.playButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.playButton.setIcon(self.playIcon)
    self.playButton.setIconSize(QSize(80,80))
    self.playButton.setStyleSheet("border: none")
    self.playLayout.addWidget(self.playButton)
    self.playButton.currentStatus = "Play"

    self.nextLayout = QVBoxLayout()
    self.nextLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.nextLayout.setContentsMargins(0,0,0,0)
    self.nextButton = QPushButton()
    self.nextButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.nextButton.setIcon(self.nextIcon)
    self.nextButton.setIconSize(QSize(80,80))
    self.nextButton.setStyleSheet("border: none")
    self.nextLayout.addWidget(self.nextButton)
        
    self.middleLayout.addLayout(self.previousLayout, 1)
    self.middleLayout.addLayout(self.playLayout, 1)
    self.middleLayout.addLayout(self.nextLayout, 1)

    self.bottomLayout.addWidget(self.middleWidget, 1)

    # Right
    self.rightWidget = QWidget()

    self.rightLayout = QHBoxLayout(self.rightWidget)
    self.rightLayout.setContentsMargins(10,10,10,10)

    self.volumeSlider = QSlider()
    self.volumeSlider.setRange(0,75) # QOL Prevents the audio getting too loud, its invonvenient
    self.volumeSlider.setValue(25)
    self.audioOutput.setVolume(self.volumeSlider.value() / 100)
    self.volumeSlider.valueChanged.connect(lambda position: self.audioOutput.setVolume(position / 100))

    self.controlsWidget = QWidget()
    self.controlsLayout = QHBoxLayout(self.controlsWidget)
    self.controlsLayout.setContentsMargins(0,0,0,0)

    self.controlsLayout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

    self.shuffleButton = QPushButton()
    self.shuffleButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.shuffleButton.setCheckable(True)
    self.shuffleButton.setStyleSheet(f"QPushButton {{border: none; border-radius:10px}} QPushButton:checked {{background-color: {colors.color3}}}")

    shufflePixmap = drawShufflePixmap()
    pauseScaledPixmap = shufflePixmap.scaled(100,100,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.shuffleButton.setIcon(QIcon(pauseScaledPixmap))
    self.shuffleButton.setIconSize(QSize(30,30))
    self.shuffleButton.setFixedSize(QSize(40,40))
    self.controlsLayout.addWidget(self.shuffleButton)
    self.shuffleButton.clicked.connect(lambda clickedStatus: self.shuffleButtonPressed(clickedStatus))

    self.reloadButton = QPushButton()
    self.reloadButton.setCursor(Qt.CursorShape.PointingHandCursor)
    self.reloadButton.setCheckable(True)
    self.reloadButton.setStyleSheet(f"QPushButton {{border: none; border-radius:10px}} QPushButton:checked {{background-color: {colors.color3}}}")
    
    reloadPixmap = drawReloadPixmap()
    reloadScaledPixmap = reloadPixmap.scaled(100,100,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.reloadButton.setIcon(QIcon(reloadScaledPixmap))
    self.reloadButton.setIconSize(QSize(30,30))
    self.reloadButton.setFixedSize(QSize(40,40))
    self.controlsLayout.addWidget(self.reloadButton)

    self.playerCountWidget = QWidget()
    self.playerCountWidget.setMinimumWidth(40)
    self.playerCountLayout = QHBoxLayout(self.playerCountWidget)
    self.playerCountLayout.setContentsMargins(0,0,0,0)
    self.playerCountLabel = QLabel()
    self.playerCountLabel.setStyleSheet("color:white; font-size:15px; font-weight:800")
    self.playerCountLayout.addWidget(self.playerCountLabel)
    self.controlsLayout.addWidget(self.playerCountWidget)

    self.rightLayout.addWidget(self.controlsWidget,1)
    self.rightLayout.addWidget(self.volumeSlider)
    self.bottomLayout.addWidget(self.rightWidget, 1)
    ## END

    self.mainLayout = QHBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.bottomWidget)

    # Button Connections
    self.playButton.clicked.connect(lambda: self.playButtonPressed())
    self.nextButton.clicked.connect(lambda: self.moveIndex(1))
    self.previousButton.clicked.connect(lambda: self.moveIndex(-1))

    # Force all elements to have the same width
    for widget in (self.leftWidget,self.songInformationWidget,self.rightWidget,):
      widget.setMinimumWidth(0)
      widget.setSizePolicy(
        QSizePolicy.Policy.Ignored,
        QSizePolicy.Policy.Preferred
      )
    
    # Variables
    self.coloredWidget = None # We store the orange widget here
    self.unshuffledPlaylist = None # We write to this if we shuffle the playlist, easy way to return back
  
  def writePlaylist(self, playlist: list):
    if playlist[0] == "single": # The play song button was pressed, decide to make a new playlist or locate the index in the existing playlist
      if self.playlist: # Locate the item inside of the playlist
        searchingData = playlist[1]
        for item in self.playlist: # Locate the index
          if item["location"] == searchingData["location"]:
            index = self.playlist.index(item)
            newIndex = index - self.playerIndex # Direction the playlist needs to be pushed by to go to the correct song
            self.moveIndex(newIndex)
            return
        playlist = [playlist[1]] # The song was not in the playlist, make a new playlist
      else:
        playlist = [playlist[1]] # Playlist was never created, make the playlist
    
    self.playlist = playlist # Replaces current playlist

    if self.shuffleButton.isChecked():
      self.shuffleButtonPressed(True)
    
    if self.coloredWidget: # Reset the song that has the "Now Playing" colour
      self.coloredWidget.mainWidget.setStyleSheet(f"background-color: {self.colors.color2}; border-radius:10px")
    
    self.playerIndex = 0 # Prevents index errors and skipped songs
    self.startPlaylist()
  
  def startPlaylist(self): # ONLY CALL THIS ON FIRST PLAY OF A PLAYLIST
    self.playerIndex = 0
    
    print("starting Playlist")
    self.writeSong(direction=1)
    
    if self.playButton.currentStatus == "Play":
      self.play()

  def playButtonPressed(self):
    isPlaying = self.player.isPlaying()
    if isPlaying:
      self.pause()
    elif self.playlist and not isPlaying:
      self.play()

  def writeSong(self, direction):
    if not os.path.exists(self.playlist[self.playerIndex]["location"]):
      print("File Deleted, moving to next song!")
      self.moveIndex(direction=direction)
    else:
      print("File exists: Playing")
      
      if self.coloredWidget:
        self.coloredWidget.mainWidget.setStyleSheet(f"background-color: {self.colors.color2}; border-radius:10px")
      
      self.coloredWidget = self.playlist[self.playerIndex]["widget"]
      self.coloredWidget.mainWidget.setStyleSheet(f"background-color: {self.colors.color5}; border-radius:10px")
      
      self.player.setSource(QUrl(self.playlist[self.playerIndex]["location"]))
      self.updateMediaDetails()

  def play(self):
    self.player.play()
    self.playButton.setIcon(self.pauseIcon)
    self.playButton.currentStatus = "Play"
  
  def pause(self):
    self.player.pause()
    self.playButton.setIcon(self.playIcon)
    self.playButton.currentStatus = "Pause"
  
  def mediaChanged(self, status):
    if str(status) == "MediaStatus.EndOfMedia":
      self.moveIndex(1)

  def endOfPlaylist(self):
    if self.reloadButton.isChecked():
      self.moveIndex((len(self.playlist)-1) * -1) # Push back to index 0 with the function (so i don't have to do the thinking)
      
      if self.shuffleButton.isChecked():
        self.shuffleButtonPressed(True) # So it reshuffles the playlist for the next loop around
      
      return
    
    print("End of playlist")
    self.playerIndex = 0
    self.playlist = []
    self.player.setSource(QUrl()) # Prevents cached music from playing
    self.playerCountLabel.setText("")
    self.player.stop()
    self.playButton.setIcon(self.playIcon)

    self.songName.setText("")
    self.artistName.setText("")
    self.albumName.setText("")

    self.albumImage.clear()
  
  def moveIndex(self, direction: int):
    newIndex = self.playerIndex + direction
    if not self.playlist or newIndex < 0: # Prevent empty playlists // Prevent going back on index 0
      return

    self.playlist[self.playerIndex]["widget"].mainWidget.setStyleSheet(f"background-color: {self.colors.color2}; border-radius:10px")
    print(newIndex)
    if newIndex >= len(self.playlist): # Reached final song of playlist
      self.endOfPlaylist()
      return
    else:
      self.playerIndex += direction
      self.writeSong(direction=direction)
      
      if self.playButton.currentStatus == "Play":
        self.play()
  
  def updateMediaDetails(self):
    songDetails = self.playlist[self.playerIndex]
    
    self.songName.setText(songDetails["name"])
    self.artistName.setText(songDetails["artist"])
    self.albumName.setText(songDetails["album"])

    self.playerCountLabel.setText(f"{self.playerIndex+1}/{len(self.playlist)}")

    albumImage = extractAlbumArt(self, songDetails["location"], 20)
    albumImageScaled = albumImage.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    self.albumImage.setPixmap(albumImageScaled)
  
  def shuffleButtonPressed(self, status):
    if status:
      if not self.player.isPlaying():
        return
      
      currentSong = self.playlist[self.playerIndex]

      self.unshuffledPlaylist = copy(self.playlist)
      
      # Shuffle the playlist partially randomly, some not
      sortedHalf = self.playlist[:self.playerIndex+1] # +1 so it includes the currently playing song
      
      unsortedHalf = self.playlist[self.playerIndex+1:] # +1 so it DOESN'T include the currently playing song
      shuffle(unsortedHalf)
      
      self.playlist = sortedHalf + unsortedHalf

      self.playerIndex = self.playlist.index(currentSong)
    else:
      if self.playlist:
        self.playerIndex = self.unshuffledPlaylist.index(self.playlist[self.playerIndex]) # Set index to where the shuffled song falls inside of the unshuffled playlist
        self.playlist = self.unshuffledPlaylist
      else:
        return # Irrelevant but edge cases are important

