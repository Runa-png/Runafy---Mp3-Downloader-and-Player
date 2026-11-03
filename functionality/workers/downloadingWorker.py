from PyQt6.QtCore import (
  Qt,
  QRunnable,
  pyqtSlot,
  pyqtSignal,
  QObject
)

from functionality.functions.download.downloadAudio import downloadAudio
from functionality.functions.download.writeAlbumArt import writeAlbumArt

import math
import sqlite3

class downloadFileWorker(QRunnable):
  class WorkerSignals(QObject):
    FINISHED = pyqtSignal()
    COUNT = pyqtSignal(int)
  
  def __init__(self, data):
    super().__init__()
    self.signals = self.WorkerSignals()
    self.songs = data
    self.running = True

    self.output = "cache"

  @pyqtSlot()
  def run(self):
    startCount = 0
    endCount = len(self.songs)
    
    print("Downloading File")

    for key in self.songs:
      if not self.running:
        return
      
      data = self.songs[key]["data"]

      fileName = f"{data["name"]} {data["album"]}"
      
      self.options = {
        "cookiesfrombrowser": ("firefox",), # Change this to your preferred browser
        "format": "bestaudio/best",
        "outtmpl": f'{self.output}/{fileName}',
        "quiet": True,
        "postprocessors": [
          {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
          }
        ],
      }

      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()
      exists = cursor.execute("SELECT * FROM songs WHERE name = ? AND artist = ?",(data["name"], data["artist"])).fetchone()

      if not exists:
        url = data["url"]
        response = downloadAudio(self, url, key)

        if response:
          self.songs[key]["downloadData"] = {"fileLocation": f"cache/{fileName}.mp3", "fileName": f"{fileName}.mp3"}
          self.songs[key]["widget"].songName.setStyleSheet("color: lime; font-size:18px; font-weight:600")
          writeAlbumArt(self.songs[key]["downloadData"]["fileLocation"], self.songs[key]["data"]["trackId"])
        else:
          self.songs[key]["widget"].songName.setStyleSheet("color: red; font-size:18px; font-weight:600")
      else:
        self.songs[key]["downloadData"] = None
        self.songs[key]["widget"].songName.setStyleSheet("color: yellow; font-size:18px; font-weight:600")
      
      startCount += 1
      self.signals.COUNT.emit(math.floor((startCount / endCount) * 100))

    self.signals.FINISHED.emit()