from .insn import from_bytes

class RiscVLifter(object):
    def __init__(self, XLen, FLen=None):
        self.XLen = XLen
        self.FLen = FLen

    def get_insn_low_level_il(self, data, addr, il):
        insn = from_bytes(data, addr, self.XLen, self.FLen)
        if insn is None:
            return None
        return insn.lift_insn(addr, il)
