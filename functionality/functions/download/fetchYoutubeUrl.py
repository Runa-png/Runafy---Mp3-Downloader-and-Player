import yt_dlp
from fuzzywuzzy import fuzz
from math import floor
from pandas import isna

def findYoutubeUrl(self, data):
  options = {
    "quiet": True,
    "nowarnings": True,
    "noplaylist": True,
    "extract_flat": True
  }
  
  # Some songs have multiple artists, split them.
  try:
    artistList = data["artist"].split(",")
  except AttributeError: # Happens if no song artist is present
    return

  if (isna(data["name"]) or isna(data["artist"]) or isna(data["album"])): # Track id is ignored, we replace with a placeholder
    return
  
  print(f"DATA: {isna(data["name"]) , isna(data["artist"]) , isna(data["album"]) , isna(data["trackId"])}")

  # Find the URL
  with yt_dlp.YoutubeDL(options) as ydl:
    # Iterate over each artist
    accuracyList = []
    for artist in artistList:
      query = data["name"] + " " + artist

      results = ydl.extract_info(
        f"ytsearch5:{query}",
        download = False
      )
      audio = results.get("entries", [])
    
      # Calculate the accuracy of the result
      for instance in audio:
        resultName = instance.get("title")
        resultArtist = instance.get("uploader")
        resultID = instance.get("id")

        nameRatio = fuzz.ratio(resultName, data["name"])
        artistRatio = fuzz.ratio(resultArtist, artist)
        totalRatio = floor((nameRatio + artistRatio) / 2)

        accuracyList.append({"id": resultID, "ratio": totalRatio, "uploader": resultArtist})
      
    # Find the highest accuracy
    highestAccuracy = {"ratio": -1}
    for songResult in accuracyList:
      if songResult["ratio"] > highestAccuracy["ratio"]:
        highestAccuracy = songResult
    
    data["ratio"] = highestAccuracy["ratio"]
    data["id"] = highestAccuracy["id"]
    data["uploader"] = highestAccuracy["uploader"]
    data["url"] = "https://www.youtube.com/watch?v=" + highestAccuracy["id"]
    
    return data