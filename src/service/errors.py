from enum import IntEnum


class ErrorCode(IntEnum):
    OTHER = 1
    ILLEGAL_INPUT = 2
    MODEL_DATA_NOT_FOUND = 3
    MODEL_URI_NOT_FOUND = 4


class ModelStoreError(Exception):
    error_code = ErrorCode.OTHER


class IllegalInput(ModelStoreError):
    error_code = ErrorCode.ILLEGAL_INPUT


class ModelDataNotFound(ModelStoreError):
    error_code = ErrorCode.MODEL_DATA_NOT_FOUND


class ModelUriNotFound(ModelStoreError):
    error_code = ErrorCode.MODEL_URI_NOT_FOUND
