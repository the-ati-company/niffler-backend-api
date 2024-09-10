from enum import Enum


class AvailableOS(Enum):
    IOS = "IOS"
    ANDROID = "ANDROID"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: str):
        value = value.upper()
        if value in [os.value for os in cls]:
            return cls(value)
        return cls.UNKNOWN
