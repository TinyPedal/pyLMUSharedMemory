"""
LMU API Enums mapping, with fast dict lookup function
"""

from __future__ import annotations

import enum

from ._common import enum_map


class LMUVehicleClass(enum.Enum):
    """Vehicle class name (mVehicleClass)"""

    Hypercar = 0x00
    LMP2_ELMS = 0x02
    LMP2 = enum.auto()
    LMP3 = enum.auto()
    GTE = enum.auto()
    GT3 = enum.auto()
    PaceCar = 0x08
    Unknown = 0xFF


class LMUVehicleChampionship(enum.Enum):
    """Vehicle championship name (mVehicleChampionship)"""

    WEC_2023 = 0x00
    WEC_2024 = enum.auto()
    WEC_2025 = enum.auto()
    WEC_2026 = enum.auto()
    ELMS_2025 = 0x10
    ELMS_2026 = enum.auto()
    Unknown = 0xFF


class LMUGameMode(enum.Enum):
    """Game mode (mGameMode)"""

    Server = 1
    Client = 2
    ServerAndClient = 3


class LMUGamePhase(enum.Enum):
    """Game phase states (mGamePhase)

    0=Before session has begun,
    1=Reconnaissance laps (race only),
    2=Grid walk-through (race only),
    3=Formation lap (race only),
    4=Starting-light countdown has begun (race only),
    5=Green flag,
    6=Full course yellow / safety car,
    7=Session stopped,
    8=Session over,
    9=Paused (tag.2015.09.14 - this is new, and indicates that this is a heartbeat call to the plugin)
    """

    Garage = 0
    WarmUp = 1
    GridWalk = 2
    Formation = 3
    Countdown = 4
    GreenFlag = 5
    FullCourseYellow = 6
    SessionStopped = 7
    SessionOver = 8
    PausedOrHeartbeat = 9


class LMUYellowFlagState(enum.Enum):
    """Yellow flag states (mYellowFlagState), applies to full-course only

    -1=Invalid,
    0=None,
    1=Pending,
    2=Pits closed,
    3=Pit lead lap,
    4=Pits open,
    5=Last lap,
    6=Resume,
    7=Race halt (not currently used)
    """

    Invalid = -1
    NoFlag = 0
    Pending = 1
    PitClosed = 2
    PitLeadLap = 3
    PitOpen = 4
    LastLap = 5
    Resume = 6
    RaceHalt = 7


class LMUSurfaceType(enum.Enum):
    """Surface type (mSurfaceType)"""

    Dry = 0
    Wet = 1
    Grass = 2
    Dirt = 3
    Gravel = 4
    Kerb = 5
    Special = 6


class LMUSession(enum.Enum):
    """Session type (mSession)"""

    TestDay = 0
    Practice1 = 1
    Practice2 = 2
    Practice3 = 3
    Practice4 = 4
    Qualifying1 = 5
    Qualifying2 = 6
    Qualifying3 = 7
    Qualifying4 = 8
    Warmup = 9
    Race1 = 10
    Race2 = 11
    Race3 = 12
    Race4 = 13


class LMUSector(enum.Enum):
    """Sector index (mSector)

    0=sector3,
    1=sector1,
    2=sector2 (don't ask why)
    """

    Sector3 = 0
    Sector1 = 1
    Sector2 = 2


class LMUFinishStatus(enum.Enum):
    """Finish status (mFinishStatus)"""

    _None = 0
    Finished = 1
    Dnf = 2
    Dq = 3


class LMUControl(enum.Enum):
    """Who's in control (mControl)

    -1=nobody (shouldn't get this),
    0=local player,
    1=local AI,
    2=remote,
    3=replay (shouldn't get this)
    """

    Nobody = -1
    Player = 0
    AI = 1
    Remote = 2
    Replay = 3


class LMUPitState(enum.Enum):
    """Pit state (mPitState)"""

    _None = 0
    Request = 1
    Entering = 2
    Stopped = 3
    Exiting = 4


class LMUPrimaryFlag(enum.Enum):
    """Primary flag being shown to vehicle (mFlag)"""

    Green = 0
    Blue = 6


class LMUCountLapFlag(enum.Enum):
    """Count lap flag (mCountLapFlag)"""

    DoNotCountLapOrTime = 0
    CountLapButNotTime = 1
    CountLapAndTime = 2


class LMURearFlapLegalStatus(enum.Enum):
    """Rear flap (DRS) status (mRearFlapLegalStatus)"""

    Disallowed = 0
    DetectedButNotAllowedYet = 1
    Alllowed = 2


class LMUIgnitionStarterStatus(enum.Enum):
    """Ignition starter status (mIgnitionStarter)"""

    Off = 0
    Ignition = 1
    IgnitionAndStarter = 2


class LMUWiperStatus(enum.Enum):
    """Wiper status (mWiperState)"""

    Off = 0
    Auto = 1
    Slow = 2
    Fast = 3


class LMUWheelIndex(enum.Enum):
    """Wheel index reference for 'LMUWheel'"""

    FrontLeft = 0
    FrontRight = 1
    RearLeft = 2
    RearRight = 3


class LMUCompoundType(enum.Enum):
    """Tyre compound type (mCompoundType)"""

    Soft = 0
    Medium = 1
    Hard = 2
    Wet = 3


class LMUTrackGripLevel(enum.Enum):
    """Track grip rubber level (mTrackGripLevel)"""

    Green = 0
    Low = 1
    Medium = 2
    High = 3
    Saturated = 4


class LMUCloudCoverage(enum.Enum):
    """Cloud coverage (mCloudCoverage)"""

    Clear = 0
    LightClouds = 1
    PartiallyCloudy = 2
    MostlyCloudy = 3
    Overcast = 4
    CloudyAndDrizzle = 5
    CloudyAndLightRain = 6
    OvercastAndLightRain = 7
    OvercastAndRain = 8
    OvercastAndHeavyRain = 9
    OvercastAndStorm = 10
