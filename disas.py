from .insn import from_bytes

class RiscVDisassembler(object):
    def __init__(self, XLen, FLen=None):
        self.XLen = XLen
        self.FLen = FLen

    def get_insn_info(self, data, addr):
        insn = from_bytes(data, addr, self.XLen, self.FLen)
        if insn is None:
            return None
        return insn.get_info(addr)

    def get_insn_text(self, data, addr):
        insn = from_bytes(data, addr, self.XLen, self.FLen)
        if insn is None:
            return None
        return insn.get_text(addr)
