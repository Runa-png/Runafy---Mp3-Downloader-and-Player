import sqlite3
import os

def validate():
  print("Validating!!!")

  connection = sqlite3.connect("database.db")
  connection.execute("PRAGMA foreign_keys = ON") # If we delete something then we need all entries removed
  cursor = connection.cursor()

  path = "music"

  # Delete Files that shouldn't be in music folder
  for file in os.scandir(path):
    filePath = file.path
    
    if not filePath.endswith(".mp3"):
      os.remove(filePath) # Why would you put a non mp3 file in music ??
      print("Removed INVALID: ", filePath)
    
    else:
      valid = cursor.execute("SELECT * FROM songs WHERE location = ?", (filePath,)).fetchone()
      
      if not valid: # The mp3 object is an IMPOSTER, GET IT GONE
        os.remove(filePath)
        print("Removed IMPOSTER: ", filePath)

  # Delete entries in DB when the file doesn't exist
  locations = cursor.execute("SELECT location FROM songs")
  deletionCursor = connection.cursor()
  for location in locations:
    if not os.path.exists(location[0]):
      print("Location NONEXISTANT: ", location[0])
      deletionCursor.execute("DELETE FROM songs WHERE location = ?", (location[0],))

