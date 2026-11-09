from fuzzywuzzy import fuzz

def sortPlaylist(playlist, name):
  for song in playlist:
    songName = song["name"]
    ratio = fuzz.ratio(songName.lower(), name)
    song["ratio"] = ratio

  playlist.sort(key=lambda song: song["ratio"], reverse=True)