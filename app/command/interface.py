from abc import ABC, abstractmethod

from app.shell_api import ShellAPI


class ICommand(ABC):
    @abstractmethod
    def run(self, api: ShellAPI):
        pass
