import sqlite3

def readPlaylists():
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  cursor.row_factory = sqlite3.Row # You can now index the results as a dict

  data = cursor.execute("SELECT * FROM playlists").fetchall()

  playlists = {}
  
  for song in data:
    songDataSQL = cursor.execute("SELECT * FROM songs WHERE location = ?", (song[1],)).fetchall()

    songData = dict(songDataSQL[0])
    
    try:
      playlists[song[0]].append(songData) # Append song location to name of the playlist
    except KeyError: # New playlist item
      playlists[song[0]] = [] # Create playlist item
      playlists[song[0]].append(songData) # Repeat

  return dict(reversed(list(playlists.items()))) # Put newest playlists first 