"""Modulo for the base repository abstract class."""
from abc import ABC, abstractmethod


class UserReporitory(ABC):
    @abstractmethod
    def get_user(self, user_id: str):
        pass

    @abstractmethod
    def create_user(self, user_data: dict):
        pass

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass
