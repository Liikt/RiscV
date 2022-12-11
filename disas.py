from binaryninja.function import InstructionTextToken, InstructionTextTokenType

from .insn import from_bytes

class RiscVDisassembler(object):
    def __init__(self, XLen, FLen=None):
        self.XLen = XLen
        self.FLen = FLen

    def get_insn_info(self, data, addr):
        insn = from_bytes(data, addr)
        if insn is not None:
            return insn.get_info(addr)
        return None

    def get_insn_text(self, data, addr):
        return [InstructionTextToken(InstructionTextTokenType.TextToken, "HELLO!")], 4