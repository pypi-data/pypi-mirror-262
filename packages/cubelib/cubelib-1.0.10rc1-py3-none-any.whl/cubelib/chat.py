from typing import Tuple
from enum import Enum
from dataclasses import dataclass
from itertools import zip_longest
import re


RESET = "\u001b[0m"

class Colors(Enum):
    BLACK = 0x0
    DARK_BLUE = 0x1
    DARK_GREEN = 0x2
    DARK_CYAN = 0x3
    DARK_RED = 0x4
    PURPLE = 0x5
    GOLD = 0x6
    GRAY = 0x7
    DARK_GRAY = 0x8
    BLUE = 0x9
    GREEN = 0xa
    CYAN = 0xb
    RED = 0xc
    PINK = 0xd
    YELLOW = 0xe
    WHITE = 0xf

@dataclass
class Color:
    id: int
    name: str
    rgb: Tuple[int, int, int]

def rgb_to_ascii(rgb: Tuple[int, int, int]):
    return "\x1b[38;2;%sm" % ";".join(map(str, rgb))

class colors:
    colors = [
        Color(*(0x0, "black", (37, 37, 37))),
        Color(*(0x1, "dark_blue", (0, 0, 242))),
        Color(*(0x2, "dark_green", (0, 170, 0))),
        Color(*(0x3, "dark_aqua", (0, 170, 170))),
        Color(*(0x4, "dark_red", (170, 0, 0))),
        Color(*(0x5, "dark_purple", (170, 0, 170))),
        Color(*(0x6, "gold", (255, 170, 0))),
        Color(*(0x7, "gray", (170, 170, 170))),
        Color(*(0x8, "dark_gray", (85, 85, 85))),
        Color(*(0x9, "blue", (85, 85, 255))),
        Color(*(0xa, "green", (85, 255, 85))),
        Color(*(0xb, "aqua", (85, 255, 255))),
        Color(*(0xc, "red", (255, 85, 85))),
        Color(*(0xd, "light_purple", (255, 85, 255))),
        Color(*(0xe, "yellow", (255, 255, 85))),
        Color(*(0xf, "white", (255, 255, 255))),
    ]

    @classmethod
    def get_by_id(cls, id: int):
        for color in cls.colors:
            if color.id == id:
                return color
        return None
    
    @classmethod
    def get_by_name(cls, name: str):
        for color in cls.colors:
            if color.name == name:
                return color
        return None


class Chat:
    json: dict

    @classmethod    
    def loads(cls, json: dict):
        instance = object.__new__(cls)
        instance.json = json
        return instance

    def ansi(self) -> str:
        """Return internal chat object as ANSI string
        """

        if "translate" in self.json:
            return str(self)

        out = ""
        base_color = ""

        if "color" in self.json:                                    
            base_color = rgb_to_ascii(colors.get_by_name(self.json["color"]).rgb)
            out += base_color

        out += self.json["text"]

        if "extra" in self.json:            
            for block in self.json["extra"]:
                if isinstance(block, str):
                    out += block
                    continue

                if "obfuscated" in block and block["obfuscated"]:
                    out += len(block["text"]) * " "
                    continue

                if "color" in block:
                    color = colors.get_by_name(block["color"])
                    out += rgb_to_ascii(color.rgb) if color else ""
                else:
                    out += base_color

                if "bold" in block and block["bold"]:
                    out += "\033[1m"
                if "italic" in block and block["italic"]:
                    out += "\033[3m"
                if "underlined" in block and block["underlined"]:
                    out += "\033[4m"
                if "strikethrough" in block and block["strikethrough"]:
                    out += "\033[9m"

                out += block["text"]
                out += RESET

        return out + RESET
    
    def __str__(self):
        if "translate" in self.json:
            if len(self.json["with"]) != 2:
                print("RARE transalte with 'with' len != 2. open issue!")
            tt = self.json["translate"]
            
            username = self.json["with"][0]["text"]
            msg = Chat.loads(self.json["with"][1])

            if tt == "chat.type.text":
                out = f"<{username}> {msg}"

            elif tt == "chat.type.emote":
                out = f"* {username} {msg}"
            
            elif tt == "chat.type.announcement":
                out = f"[{username}] {msg}"

            return out

        out = self.json["text"]

        if "extra" in self.json:
            for block in self.json["extra"]:
                if isinstance(block, str):
                    out += block
                    continue
                if "obfuscated" in block:
                    if block["obfuscated"]:
                        out += len(block["text"]) * " "
                        continue

                out += block["text"]

        return out
    
    @classmethod
    def from_old(cls, text: str, lit: str = "§"):
        instance = object.__new__(cls)
        instance.json = {"text": "", "extra": []}
        
        ma = re.findall(lit + "([0-z])", text)
        sp = re.split(lit + "[0-z]", text)
        # print(ma, sp)

        components = []
        curr = {"text": sp[0]}

        for modifier, s in zip_longest(ma, sp[1:]):  
            # print(modifier, s)
            if modifier in "klmnor":
                if curr["text"]:
                    # flush
                    components.append(curr)
                    curr = curr.copy()
                    del curr["text"]

                if modifier == "k":
                    curr["text"] = len(s) * " "
                    curr["obfuscated"] = True
                else:                    
                    curr["text"] = s

                if modifier == "n":
                    curr["underlined"] = True
                elif modifier == "l":
                    curr["bold"] = True
                elif modifier == "o":
                    curr["italic"] = True
                elif modifier == "m":
                    curr["strikethrough"] = True
                elif modifier == "r":
                    curr.pop("bold", None)
                    curr.pop("italic", None)
                    curr.pop("underlined", None)
                    curr.pop("obfuscated", None)
                    curr.pop("strikethrough", None)
                    curr.pop("color", None)
                    
            else:
                if curr["text"]:
                    # flush
                    components.append(curr)
                    curr = curr.copy()
                    del curr["text"]
                curr["color"] = colors.get_by_id(int(modifier, 16)).name
                curr["text"] = s
                curr.pop("underlined", None)
            
            # print(curr)
        components.append(curr)
        instance.json["extra"] = components
        return instance

def minecraft_uncolorize(text: str) -> str:    
    return re.sub("§[0-z]", "", text)

def minecraft_colorized_text(text: str):    
    chat = Chat.from_old(text)
    return chat.ansi()
