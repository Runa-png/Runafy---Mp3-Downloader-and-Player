from csv import reader

def readCSV(location):
  print(location)

  CSVUnformattedList = []
  with open(location, "r") as file:
    CSV = reader(file)
  
    for row in CSV:
      CSVUnformattedList.append(row)
    
  columnIndexes = CSVUnformattedList[0]
  CSVUnformattedList.pop(0)
  
  formattedCSV = []
  for song in CSVUnformattedList:
    newData = {}
    
    for column, songData in zip(columnIndexes, song): # Iterate over both columns and songs in the same index
      newData[column] = songData
    
    formattedCSV.append(newData)
        
  return formattedCSV