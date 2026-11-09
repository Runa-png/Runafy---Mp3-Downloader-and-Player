from PyQt6.QtWidgets import (
  QApplication
)
from functionality.mainWindow import MainWindow
from functionality.initialise import initialise
from functionality.validate import validate

from shutil import rmtree
from os import makedirs
from sys import argv

def main():
  app = QApplication(argv)
  window = MainWindow()
  window.show()
  app.exec()

if __name__ == '__main__':
  rmtree("cache", ignore_errors=True)
  makedirs("music", exist_ok=True)
  initialise()
  validate() # Issues in the database can cause crashes, validate them
  
  main()

