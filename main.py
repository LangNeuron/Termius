# main.py


if __name__ == "__main__":
    from signals import Signals
    from core import Core

    signals = Signals()
    core = Core(signals=signals)
    core.run()
