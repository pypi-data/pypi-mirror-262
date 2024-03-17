from importlib.metadata import version

from .Bot import Bot

from .core import websocket
from .core.experimental import aiows
from .core.types import *  # noqa: F403
from .core.types import drive, note, poll, user
from .settings import Option, extension  # noqa: F401

__version__ = version("misspy")

MSC = aiows.MSC  # Misskey
MIWS_V2 = websocket.MiWS_V2

homeTimeline = "homeTimeline"
localTimeline = "localTimeline"
socialTimeline = "hybridTimeline"
hybridTimeline = "hybridTimeline"
globalTimeline = "globalTimeline"

Note = note.Note

DriveFolder = drive.DriveFolder
df_property = drive.df_property
DriveFile = drive.DriveFile

avatarDecorations = user.AvatarDecorations
User = user.User
UserLite = user.UserLite

Poll = poll.Poll


class visibility:
    public = "public"
    home = "home"
    followers = "followers"
    specified = "specified"
