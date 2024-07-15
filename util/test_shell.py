from app.advanced_logic import AdvancedLogic
from app.test_shell_app import TestShellApp

if __name__ == '__main__':
    logic = AdvancedLogic()
    app = TestShellApp(logic)
    while True:
        inp = input()
        exit_condition = app.run(inp)
        if exit_condition:
            break
