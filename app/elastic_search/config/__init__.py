from enum import Enum


class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @classmethod
    def has_key(cls, key):
        return key in cls.__members__

    @classmethod
    def get_description(cls) -> str:
        keys = [key for key in cls.__members__.values()]
        keys_str = ", ".join(keys)
        return f"Available values: {keys_str[:-2]}"
