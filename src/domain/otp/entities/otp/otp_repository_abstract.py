from abc import ABC, abstractmethod
from typing import Optional
from domain.otp.entities.otp.otp import OTP


class OTPRepositoryAbstract(ABC):
    @abstractmethod
    def save(self, otp: OTP) -> None:
        pass

    @abstractmethod
    def get(self, to: str) -> Optional[OTP]:
        pass
