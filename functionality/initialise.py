import sqlite3

def initialise():
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()

  cursor.execute("CREATE TABLE IF NOT EXISTS songs (name TEXT, artist TEXT, album TEXT, location TEXT PRIMARY KEY)")
  cursor.execute("CREATE TABLE IF NOT EXISTS playlists (playlistName TEXT, location TEXT, FOREIGN KEY (location) REFERENCES songs(location) ON DELETE CASCADE)")

  connection.commit()
  connection.close()
