from app.advanced_logic import AdvancedLogic


class TestShellApp:
    _logic: AdvancedLogic

    def __init__(self, logic: AdvancedLogic):
        self._logic = logic

    def run(self, line) -> bool:
        # Call _app.methods
        # return True for exit condition
        return True


if __name__ == '__main__':
    logic = AdvancedLogic()
    app = TestShellApp(logic)
    while True:
        inp = input()
        exit_condition = app.run(inp)
        if exit_condition:
            break
