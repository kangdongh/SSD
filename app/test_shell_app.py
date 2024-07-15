from app.advanced_logic import AdvancedLogic


class TestShellApp:
    _logic: AdvancedLogic

    def __init__(self, logic: AdvancedLogic):
        self._logic = logic

    def run(self, line) -> bool:
        # Call _app.methods
        # return True for exit condition
        return True
