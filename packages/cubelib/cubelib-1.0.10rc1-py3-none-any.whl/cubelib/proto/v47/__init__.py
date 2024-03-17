from . import ClientBound, ServerBound
from .enums import *
from .world import *

name = 'Minecraft Java Edition protocol version 47'
version = 47
capabilities = [
    "chunk",
    "slot",
    "emeta",
    "chat"
]
