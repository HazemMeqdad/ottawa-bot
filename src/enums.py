from enum import Enum


class ComponentTypes(Enum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3


class ApplicationCommandTypes(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ButtonStyles(Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCRSS = 3
    DANGER = 4
    LINK = 5
