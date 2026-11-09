from PyQt6.QtWidgets import (
  QWidget,
  QHBoxLayout,
  QVBoxLayout,
  QLabel,
  QToolBar,
  QToolButton,
  QMenu
)

from PyQt6.QtCore import (
  Qt,
  pyqtSignal
)

from PyQt6.QtGui import QAction

class TopSection(QWidget):
  DROPDOWN_PRESSED = pyqtSignal(str)
  
  def __init__(self, colors):
    super().__init__()

    self.topWidget = QWidget()
    self.topWidget.setContentsMargins(0,0,0,0)
    self.topWidget.setStyleSheet(f"background-color: {colors.color1}")
    self.topWidget.setFixedHeight(40)
    self.topLayout = QVBoxLayout(self.topWidget)
    self.topLayout.setSpacing(0)
    self.topLayout.setContentsMargins(0,0,0,0)

    # Toolbar
    self.toolbar = QToolBar("main toolbar")
    self.toolbar.setStyleSheet(f"color: {colors.text1}; font-size: 15px")
    self.toolbar.setContentsMargins(0,0,0,0)
    self.toolbar.setFixedHeight(40)

    spacer = QWidget()
    spacer.setFixedWidth(20)

    # File dropdown
    self.fileButton = QToolButton()
    self.fileButton.setFixedSize(50,30)
    self.fileButton.setText("Music")
    self.fileButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
    self.fileButton.setStyleSheet(f"QMenu::item:selected {{background-color: rgb(255,255,255); color: {colors.text1}}}")
    self.fileMenu = QMenu(self.fileButton)
    self.downloadMusic = self.fileMenu.addAction("Download Music")
    self.manageMusic = self.fileMenu.addAction("Manage Music")
    self.fileButton.setMenu(self.fileMenu)
    self.toolbar.addWidget(self.fileButton)

    self.downloadMusic.triggered.connect(lambda option: self.DROPDOWN_PRESSED.emit("DOWNLOAD MUSIC"))
    self.manageMusic.triggered.connect(lambda option: self.DROPDOWN_PRESSED.emit("MANAGE MUSIC"))

    self.toolbar.addWidget(spacer)

    # Playlist dropdown
    self.playlistButton = QToolButton()
    self.playlistButton.setFixedSize(60,30)
    self.playlistButton.setText("Playlist")
    self.playlistButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
    self.playlistButton.setStyleSheet(f"QMenu::item:selected {{background-color: rgb(255,255,255); color: {colors.text1}}}")
    self.playlistMenu = QMenu(self.playlistButton)
    self.createPlaylist = self.playlistMenu.addAction("Create Playlist")
    self.managePlaylist = self.playlistMenu.addAction("Manage Playlists")
    self.playlistButton.setMenu(self.playlistMenu)
    self.toolbar.addWidget(self.playlistButton)
    
    self.createPlaylist.triggered.connect(lambda option: self.DROPDOWN_PRESSED.emit("CREATE PLAYLIST"))
    self.managePlaylist.triggered.connect(lambda option: self.DROPDOWN_PRESSED.emit("MANAGE PLAYLIST"))
    
    self.topLayout.addWidget(self.toolbar)

    self.mainLayout = QHBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.addWidget(self.topWidget)