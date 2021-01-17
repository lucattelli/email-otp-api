from abc import ABC, abstractmethod
from typing import Optional
from domain.otp.entities.otp.otp import OTP


class OTPRepositoryAbstract(ABC):
    @abstractmethod
    def save(self, otp: OTP) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def get(self, to: str) -> Optional[OTP]:
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, to: str) -> None:
        pass  # pragma: no cover
