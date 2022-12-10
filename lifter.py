from binaryninja import LLIL_TEMP, Architecture, LowLevelILLabel, log_error, log_warn, LowLevelILFunction

from .disas import RiscVInstruction

_unliftable = {"reserved"}

class RiscVLifter(object):
    def __init__(self, XLen, FLen=None) -> None:
        pass