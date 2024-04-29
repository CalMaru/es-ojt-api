from app.model.enum import KorEnum


class ProviderType(KorEnum):
    ALL = "전체"
    CATEGORY = "유형별"
    DETAIL = "언론사 분류순"
    LOCAL = "지역언론사별"
    ALPHABETIC = "가나다순"
