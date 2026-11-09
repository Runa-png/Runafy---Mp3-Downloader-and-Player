from sqlite3 import connect
from os import scandir, remove, path

def validate():
  print("Validating!!!")

  connection = connect("database.db")
  connection.execute("PRAGMA foreign_keys = ON") # If we delete something then we need all entries removed
  cursor = connection.cursor()

  scanDir = "music"

  # Delete Files that shouldn't be in music folder
  for file in scandir(scanDir):
    filePath = file.path
    
    if not filePath.endswith(".mp3"):
      remove(filePath) # Why would you put a non mp3 file in music ??
      print("Removed INVALID: ", filePath)
    
    else:
      valid = cursor.execute("SELECT * FROM songs WHERE location = ?", (filePath,)).fetchone()
      
      if not valid: # The mp3 object is an IMPOSTER, GET IT GONE
        remove(filePath)
        print("Removed IMPER: ", filePath)

  # Delete entries in DB when the file doesn't exist
  locations = cursor.execute("SELECT location FROM songs")
  deletionCursor = connection.cursor()
  for location in locations:
    if not path.exists(location[0]):
      print("Location NONEXISTANT: ", location[0])
      deletionCursor.execute("DELETE FROM songs WHERE location = ?", (location[0],))

