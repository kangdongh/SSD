from abc import ABC, abstractmethod
from typing import Optional

from app.return_code import ReturnCode
from app.shell_api import ShellAPI


class ICommand(ABC):

    def safe_run(self, api: ShellAPI) -> ReturnCode:
        try:
            return_code = self.run(api)
        except Exception as e:
            print(e)
            return ReturnCode.FAILURE
        if isinstance(return_code, ReturnCode):
            return return_code
        return ReturnCode.SUCCESS

    @abstractmethod
    def run(self, api: ShellAPI) -> Optional[ReturnCode]:
        pass

    @classmethod
    def description(cls):
        return ''

    def __repr__(self):
        return self.__class__.__name__
