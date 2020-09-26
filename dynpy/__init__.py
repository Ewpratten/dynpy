import requests
from typing import List, Dict, Generator
import time
import numpy as np

class WebChatNotEnabledException(Exception):
    def __init__(self):
        super().__init__("This server has web chat disabled")

class ChatMessage(object):
    """A message sent to the world chat"""
    player_name: str
    message: str
    timestamp: time.struct_time

class PlayerStatus(object):
    """A player's status"""
    name: str
    position: np.array
    health: float
    armor: float

class Dynmap(object):

    server: str
    configuration: dict
    last_frame: dict
    last_frame_time: int
    last_last_frame_time: int

    def __init__(self, server: str):
        self.server = server
        self.configuration = self._getServerConfiguration()
        self.last_last_frame_time = int(time.time())
        self.last_frame_time = int(time.time())


    def _getServerConfiguration(self) -> dict:
        """Gets a dynmap server's configuration file

        Returns:
            dict: Config data
        """

        # Make request
        return requests.get(f"{self.server}/up/configuration").json()
    
    def sendChatMessage(self, message: str, player: str = "unknown") -> bool:
        """Sends a chat message

        Args:
            server (str): Server to send to
            message (str): Message to send
            player (str, optional): Player name to use. Defaults to "unknown".

        Returns:
            bool: True if successful
        """

        # Throw an error if webchat is disabled
        if not self.configuration["allowwebchat"]:
            raise WebChatNotEnabledException()

        # Make request
        res = requests.post(f"{self.server}/up/sendmessage", json={
            "name": player,
            "message": message
        }).json()
        return res["error"] == "none"

    def update(self, world: str = None):
        """Makes a request to fetch a new data frame"""

        # Get the hosts timestamp
        self.last_last_frame_time = self.last_frame_time
        self.last_frame_time = int(time.time())

        # Get the overworld world name
        if not world:
            world = self.configuration["defaultworld"]

        # Make request, and save it
        self.last_frame = requests.get(f"{self.server}/up/world/{world}/{self.last_frame_time}").json()

    def getRecentChatMessages(self) -> Generator[ChatMessage, None, None]:
        """Get all recent chat messages

        Returns:
            Generator[ChatMessage, None, None]: Messages
        """

        for update in self.last_frame["updates"]:

            # Check if the update is a chat
            if update["type"] == "chat":
                # Skip it if it does not fall between the current and last timestamp
                if update["timestamp"] / 1000 <= self.last_last_frame_time:
                    continue

                # Build a chat message
                message = ChatMessage()

                message.player_name = update["playerName"]
                message.message = update["message"]
                message.timestamp = time.gmtime(update["timestamp"] / 1000)

                # Add chat message
                yield message

        return 

    def getPlayers(self) -> Generator[PlayerStatus, None, None]:
        """Gets a list of all online players

        Returns:
            Generator[PlayerStatus, None, None]: Players
        """

        for update in self.last_frame["players"]:

            # Check if the update is a chat
            if update["type"] == "player":

                # Build a player
                player = PlayerStatus()
                player.name = update["name"]
                player.position = np.array([update["x"], update["y"], update["z"]])
                player.health = update["health"]
                player.armor = update["armor"]

                
                # Add the player
                yield player
        return