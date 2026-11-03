import sys
from PyQt6.QtWidgets import (
  QApplication
)
from functionality.mainWindow import MainWindow
from functionality.initialise import initialise
from functionality.validate import validate

import shutil
import os

def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()

if __name__ == '__main__':
  shutil.rmtree("cache", ignore_errors=True)
  os.makedirs("music", exist_ok=True)
  initialise()
  validate() # Issues in the database can cause crashes, validate them
  
  main()

