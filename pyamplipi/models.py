"""AmpliPi Data Models - Extracted from the amplipi repo.
"""

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class SourceInfo(BaseModel):
    name: str
    state: str  # paused, playing, stopped, unknown, loading ???
    artist: Optional[str]
    track: Optional[str]
    album: Optional[str]
    station: Optional[str]  # name of radio station
    img_url: Optional[str]
    supported_cmds: List[str] = []


class Source(BaseModel):
    """ An audio source """
    id: Optional[int]
    name: str
    input: str
    info: Optional[SourceInfo]  # Additional info about the current audio playing from the stream (generated during
    # playback')


class SourceUpdate(BaseModel):
    """ Partial reconfiguration of an audio Source """
    name: Optional[str] = None
    input: Optional[str] = None  # 'None', 'local', 'stream=ID'


class SourceUpdateWithId(SourceUpdate):
    """ Partial reconfiguration of a specific audio Source """
    id: int


class Zone(BaseModel):
    """ Audio output to a stereo pair of speakers, typically belonging to a room """
    id: Optional[int]
    name: str
    source_id: int
    mute: bool
    vol: int
    vol_f: float
    vol_min: int
    vol_max: int
    disabled: bool


class ZoneUpdate(BaseModel):
    """ Reconfiguration of a Zone """
    name: Optional[str]
    source_id: Optional[int]
    mute: Optional[bool]
    vol: Optional[int]
    vol_f: Optional[float]
    vol_min: Optional[int]
    vol_max: Optional[int]
    disabled: Optional[bool]


class ZoneUpdateWithId(ZoneUpdate):
    """ Reconfiguration of a specific Zone """
    id: int


class MultiZoneUpdate(BaseModel):
    """ Reconfiguration of multiple zones specified by zone_ids and group_ids """
    zones: Optional[List[int]]
    groups: Optional[List[int]]
    update: ZoneUpdate


class Group(BaseModel):
    """ A group of zones that can share the same audio input and be controlled as a group ie. Upstairs. Volume, mute,
    and source_id fields are aggregates of the member zones."""
    id: Optional[int]
    name: str
    source_id: Optional[int]
    zones: List[int]
    mute: Optional[bool]
    vol_delta: Optional[int]
    vol_f: Optional[float]


class GroupUpdate(BaseModel):
    """ Reconfiguration of a Group """
    name: Optional[str]
    source_id: Optional[int]
    zones: Optional[List[int]]
    mute: Optional[bool]
    vol_delta: Optional[int]
    vol_f: Optional[float]


class GroupUpdateWithId(GroupUpdate):
    """ Reconfiguration of a specific Group """
    id: int


class Stream(BaseModel):
    """ Digital stream such as Pandora, AirPlay or Spotify """
    id: Optional[int]
    name: str
    type: str
    user: Optional[str]
    password: Optional[str]
    station: Optional[str]
    url: Optional[str]
    logo: Optional[str]
    freq: Optional[str]
    client_id: Optional[str]
    token: Optional[str]


class StreamUpdate(BaseModel):
    """ Reconfiguration of a Stream """
    name: str
    user: Optional[str]
    password: Optional[str]
    station: Optional[str]
    url: Optional[str]
    logo: Optional[str]
    freq: Optional[str]


class StreamCommand(str, Enum):
    PLAY = 'play'
    PAUSE = 'pause'
    NEXT = 'next'
    PREV = 'prev'
    STOP = 'stop'
    LOVE = 'love'
    BAN = 'ban'
    SHELVE = 'shelve'


class PresetState(BaseModel):
    """ A set of partial configuration changes to make to sources, zones, and groups """
    sources: Optional[List[SourceUpdateWithId]]
    zones: Optional[List[ZoneUpdateWithId]]
    groups: Optional[List[GroupUpdateWithId]]


class Command(BaseModel):
    """ A command to execute on a stream """
    stream_id: int
    cmd: str


class Preset(BaseModel):
    id: Optional[int]
    name: str
    state: Optional[PresetState]
    commands: Optional[List[Command]]
    last_used: Union[int, None] = None


class PresetUpdate(BaseModel):
    name: Optional[str]
    state: Optional[PresetState]
    commands: Optional[List[Command]]


class Announcement(BaseModel):
    media: str
    vol: Optional[int] = None
    vol_f: Optional[float] = None
    source_id: Optional[int] = None
    zones: Optional[List[int]] = None
    groups: Optional[List[int]] = None


class PlayMedia(BaseModel):
    media: str
    vol: Optional[int]
    vol_f: Optional[float]
    source_id: Optional[int]


class FirmwareInfo(BaseModel):
    version: Optional[str]
    git_hash: Optional[str]
    git_dirty: Optional[bool]


class Info(BaseModel):
    config_file: str = 'Uknown'
    version: str = 'Unknown'
    mock_ctrl: bool = False
    mock_streams: bool = False
    online: Optional[bool] = True
    latest_release: Optional[str]
    fw: Optional[List[FirmwareInfo]]


class Config(BaseModel):
    sources: List[Source] = []
    zones: List[Zone] = []
    groups: List[Group] = []
    streams: List[Stream] = []
    presets: List[Preset] = []


class Status(Config):
    info: Optional[Info]


class AppSettings(BaseModel):
    mock_ctrl: bool = True
    mock_streams: bool = True
    config_file: str = 'house.json'
    delay_saves: bool = True
