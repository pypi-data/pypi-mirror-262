from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QLabel, QPushButton, QLineEdit)

from .contestants import BUTTON_SIZE


class Credentials(QWidget):
    """Class entering Spotify credentials."""
    def __init__(self, interface, language, music):
        super().__init__()
        self.interface = interface

        self.id = None
        self.secret = None
        self.language = None
        self.playlist = None

        self.layout = QVBoxLayout()

        self.info()
        self.input(language, music)

        self.setLayout(self.layout)

    def info(self):
        """Adds information to the layout."""
        _information = QGroupBox("Spotify")
        information = QGroupBox()

        content = QVBoxLayout()

        steps = QLabel("1. Go to <a href='https://developer.spotify.com/dashboard/create'>"
                       "https://developer.spotify.com/dashboard/create</a><br><br>"
                       "2. Enter the following information:<br><br>"
                       "&nbsp;&nbsp;&nbsp;&nbsp;Redirect URI: http://localhost:3000/callback<br>"
                       "&nbsp;&nbsp;&nbsp;&nbsp;API: Web API<br><br>"
                       "3. Click 'Save'.<br><br>"
                       "4. Click 'Settings'.<br><br>"
                       "5. Copy the 'Client ID' and 'Client Secret' into the fields below.")
        steps.setAlignment(Qt.AlignLeft)
        steps.setOpenExternalLinks(True)
        steps.setWordWrap(True)
        steps.setStyleSheet("color: black; font-family: 'Courier New', Courier, monospace;")

        content.addWidget(steps)

        information.setLayout(content)
        information.setObjectName("information")
        information.setStyleSheet("""
            QWidget#information {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(information)
        _information.setLayout(layout)

        self.layout.addWidget(_information)

    def input(self, language, music):
        """Sets up the layout."""
        _id = music["spotify"]["client_id"] if music["spotify"]["client_id"] else None
        _secret = music["spotify"]["client_secret"] if music["spotify"]["client_secret"] else None

        _language = language if language else "en"

        playlist = music["playlist"]
        if playlist.startswith("https://open.spotify.com/playlist/"):
            playlist = playlist.split("/")[-1].split("?")[0]
        _playlist = playlist.split(":")[-1] if playlist else "6TutgaHFfkThmrrobwA2y9"

        top = QHBoxLayout()
        bottom = QHBoxLayout()

        _left = QGroupBox("Credentials")
        left = QVBoxLayout()

        id = QHBoxLayout()
        self.id = QLineEdit()
        self.id.setPlaceholderText("Spotify id")
        self.id.setText(_id)
        self.id.setFixedHeight(int(BUTTON_SIZE * 0.5))
        self.id.setAlignment(Qt.AlignCenter)
        id.addWidget(self.id)

        secret = QHBoxLayout()
        self.secret = QLineEdit()
        self.secret.setText(_secret)
        self.secret.setPlaceholderText("Spotify secret")
        self.secret.setFixedHeight(int(BUTTON_SIZE * 0.5))
        self.secret.setAlignment(Qt.AlignCenter)
        secret.addWidget(self.secret)

        left.addLayout(id)
        left.addLayout(secret)

        _left.setLayout(left)
        _left.setObjectName("left")
        _left.setStyleSheet("""
            QWidget#left {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)

        _right = QGroupBox("Settings")
        right = QVBoxLayout()

        language = QHBoxLayout()
        self.language = QLineEdit()
        self.language.setPlaceholderText("Language")
        self.language.setText(_language)
        self.language.setFixedHeight(int(BUTTON_SIZE * 0.5))
        self.language.setAlignment(Qt.AlignCenter)
        language.addWidget(self.language)

        playlist = QHBoxLayout()
        self.playlist = QLineEdit()
        self.playlist.setPlaceholderText("Playlist url or id")
        self.playlist.setText(_playlist)
        self.playlist.setFixedHeight(int(BUTTON_SIZE * 0.5))
        self.playlist.setAlignment(Qt.AlignCenter)
        playlist.addWidget(self.playlist)

        right.addLayout(language)
        right.addLayout(playlist)

        _right.setLayout(right)
        _right.setObjectName("right")
        _right.setStyleSheet("""
            QWidget#right {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)

        top.addWidget(_left)
        top.addWidget(_right)

        save = QPushButton("Save")
        save.clicked.connect(self.update)
        save.setFixedHeight(int(BUTTON_SIZE * 0.5))

        bottom.addWidget(save)

        self.layout.addStretch()
        self.layout.addLayout(top)
        self.layout.addLayout(bottom)

    def update(self):
        """Updates the credentials and swich tabs of interface."""
        self.interface.parameters["music"]["spotify"]["client_id"] = self.id.text()
        self.interface.parameters["music"]["spotify"]["client_secret"] = self.secret.text()

        playlist = self.playlist.text() if self.playlist.text() else "6TutgaHFfkThmrrobwA2y9"

        if playlist.startswith("https://open.spotify.com/playlist/"):
            playlist = playlist.split("/")[-1].split("?")[0]

        self.interface.parameters["music"] = {
            "playlist": "spotify:playlist:" + playlist,
            "spotify": {
                "client_id": self.id.text(),
                "client_secret": self.secret.text(),
                "redirect_uri": "http://localhost:3000/callback"
            }
        }

        language = self.language.text().lower() if self.language.text() else "en"
        self.interface.parameters["language"] = language

        self.interface.change(self.interface.tabs.currentIndex() + 1)
