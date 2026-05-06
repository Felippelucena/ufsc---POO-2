import sys
from src.uiTerminal import UiTerminal

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    ui = UiTerminal()
    ui.iniciar()
