from PyQt6.QtCore import (
  Qt,
  QRunnable,
  pyqtSlot,
  pyqtSignal,
  QObject
)

from functionality.functions.download.fetchYoutubeUrl import findYoutubeUrl
from functionality.functions.download.readCSV import readCSV
from functionality.functions.download.downloadSpotifyPlaylist import downloadSpotifyPlaylist

from math import floor

class fetchFileWorker(QRunnable):
  class WorkerSignals(QObject):
    URL_FOUND = pyqtSignal(dict)
    COUNT = pyqtSignal(int)
    FINISHED = pyqtSignal()
    STATUS = pyqtSignal(str)
  
  def __init__(self, location):
    super().__init__()
    self.signals = self.WorkerSignals()
    self.running = True
    self.location = location

  @pyqtSlot()
  def run(self):
    print("Executing CSV operation")
    
    CSV = readCSV(self, self.location)

    if CSV is None or CSV.empty:
      self.signals.STATUS.emit("CSV could not be loaded")
      self.signals.FINISHED.emit()
      return
    
    CSV = CSV[["Song", "Artist", "Album", "Spotify Track Id"]]
    self.searchedCSV = CSV

    self.songs = []
    for _, row in CSV.iterrows():
      songData = {"name": row["Song"], "artist": row["Artist"], "album": row["Album"], "trackId": row["Spotify Track Id"]}
      self.songs.append(songData)
    
    count = 0
    total = len(self.songs)

    self.signals.COUNT.emit(0) # Reset Progress Bar
    for song in self.songs:
      # end if the app is closed
      if not self.running:
        return
      
      url = findYoutubeUrl(self, song)

      if not url:
        self.signals.STATUS.emit("CSV is malformed")
        self.signals.FINISHED.emit()
        return
      url["index"] = count

      if url:
        self.signals.URL_FOUND.emit(url)
      
      count += 1

      percentage = floor((count / total) * 100)
      self.signals.COUNT.emit(percentage)
    
    self.signals.FINISHED.emit()
