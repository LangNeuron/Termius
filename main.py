# main.py

if __name__ == "__main__":
    import asyncio
    from signals import Signals
    from core import Core

    signals = Signals()
    core = Core(signals=signals)
    asyncio.run(core.run())
