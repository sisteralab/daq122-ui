import os
import logging

from .win_daq122 import WinDAQ122
from .lin_daq122 import LinDAQ122


def get_daq_class():
    if os.name == "posix":
        return LinDAQ122
    return WinDAQ122


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
