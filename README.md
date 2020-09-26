# dynpy

`dynpy` is a simple Python library for interfacing with a Minecraft server running [dynmap](https://www.reddit.com/r/Dynmap/).

## Installation

Installing dynpy is fairly simple. Just make sure `python3` and `python3-pip` are installed on your system, the run:

```sh
python3 -m pip install git+https://github.com/Ewpratten/dynpy.git
```

## Usage

```python
# Import the library
import dynpy
from typing import List

# Open a connection to a dynmap server
d = dynpy.Dynmap("http://dynmap.example.com:8123")

# Send a chat message
d.sendChatMessage("Hello from my Python script!")

# Get a single status update from the dynmap server
d.update()

# Get a list of all recent chat messages
recent_chats: List[dynpy.ChatMessage] = list(d.getRecentChatMessages())

for message in recent_chats:
    print(f"{message.player} -> {message.message}")

# Get a list of all online players
players: List[dynpy.PlayerStatus] = d.getPlayers()

for player in players:
    print(f"Player {player.name} is at {player.position} with {player.health} health, and {player.armor} armor")


```