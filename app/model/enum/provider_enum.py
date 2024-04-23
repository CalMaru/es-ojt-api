from enum import Enum


class ProviderType(Enum):
    CATEGORY = "유형별"
    DETAIL = "언론사 분류순"
    LOCAL = "지역언론사별"
    ALPHABETIC = "가나다순"
