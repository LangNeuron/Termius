# main.py


from signals import Signals
from core import Core

signals = Signals()
core = Core(signals=signals)

core.run()
