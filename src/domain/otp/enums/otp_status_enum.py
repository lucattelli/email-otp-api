from enum import Enum


class OTPStatusEnum(Enum):
    EXPIRED = 'expired'
    INVALID = 'invalid'
    PENDING = 'pending'
    VALIDATED = 'validated'
