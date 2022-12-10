class RiscVDisassembler(object):
    def __init__(self, XLen, FLen=None):
        self.XLen = XLen
        self.FLen = FLen

    def get_insn_info(self, data, addr):
        pass

    def get_insn_text(self, data, addr):
        pass