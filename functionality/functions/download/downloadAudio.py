from yt_dlp import YoutubeDL

def downloadAudio(self, url, index):
  breakOnError = [
    "is not a valid URL",
    "Unable to download webpage",
    "This video is unavailable",
    "Playlists",
    "Failed to resolve"
  ]
  
  passed = False
  while not passed:
    try:
      with YoutubeDL(self.options) as ydl:
        ydl.download(url)
        passed = True
    except Exception as e:
      errorMessage = str(e)
      print(f"EXCEPTION: {e}")

      if any(error in errorMessage for error in breakOnError):
        return False
  
  return True