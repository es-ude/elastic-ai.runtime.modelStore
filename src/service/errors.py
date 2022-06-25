from enum import IntEnum


class ErrorCode(IntEnum):
    OTHER = 1
    ILLEGAL_INPUT = 2
    MODEL_NOT_FOUND = 3


class ModelStoreError(Exception):
    error_code = ErrorCode.OTHER


class IllegalInput(ModelStoreError):
    error_code = ErrorCode.ILLEGAL_INPUT


class ModelNotFound(ModelStoreError):
    error_code = ErrorCode.MODEL_NOT_FOUND
