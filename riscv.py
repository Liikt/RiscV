from binaryninja import Architecture, Endianness, RegisterInfo

from .disas import RiscVDisassembler
from .lifter import RiscVLifter


GP_REGS = ["zero", "ra", "sp", "gp", "tp"] + \
    [f"s{x}"  for x in range(12)] + \
    [f"a{x}"  for x in range(8)]  + \
    [f"t{x}"  for x in range(7)]

FP_REGS = [f"fs{x}" for x in range(12)] + \
    [f"fa{x}" for x in range(8)]  + \
    [f"ft{x}" for x in range(12)]


class RiscV32(Architecture):
    name = "riscv32"

    default_int_size = 4
    max_instr_length = 4

    endianness = Endianness.LittleEndian

    disassembler = RiscVDisassembler(4)
    lifter = RiscVLifter(4)

    regs = {x: RegisterInfo(x, 4) for x in GP_REGS}
    stack_pointer = "sp"

    def get_instruction_info(self, data, addr):
        self.disassembler.get_insn_info(data, addr)

    def get_instruction_text(self, data, addr):
        self.disassembler.get_insn_text(data, addr)

    def get_instruction_low_level_il(self, data, addr, il):
        self.lifter.lift_insn(data, addr, il)

class RiscV32F(RiscV32):
    name = "riscv32f"
    RiscV32.regs.update({x: RegisterInfo(x, 4) for x in FP_REGS})

    disassembler = RiscVDisassembler(4, 4)
    lifter = RiscVLifter(4, 4)

class RiscV32D(RiscV32):
    name = "riscv32d"
    RiscV32.regs.update({x: RegisterInfo(x, 8) for x in FP_REGS})

    disassembler = RiscVDisassembler(4, 8)
    lifter = RiscVLifter(4, 8)

class RiscV32Q(RiscV32):
    name = "riscv32q"
    RiscV32.regs.update({x: RegisterInfo(x, 16) for x in FP_REGS})

    disassembler = RiscVDisassembler(4, 16)
    lifter = RiscVLifter(4, 16)


class RiscV64(RiscV32):
    name = "riscv64"
    regs = {x: RegisterInfo(x, 8) for x in GP_REGS}

    disassembler = RiscVDisassembler(8)
    lifter = RiscVLifter(8)

class RiscV64F(RiscV64):
    name = "riscv64f"
    RiscV64.regs.update({x: RegisterInfo(x, 4) for x in FP_REGS})

    disassembler = RiscVDisassembler(8, 4)
    lifter = RiscVLifter(8, 4)

class RiscV64D(RiscV64):
    name = "riscv64d"
    RiscV64.regs.update({x: RegisterInfo(x, 8) for x in FP_REGS})

    disassembler = RiscVDisassembler(8, 8)
    lifter = RiscVLifter(8, 8)

class RiscV64Q(RiscV64):
    name = "riscv64q"
    RiscV32.regs.update({x: RegisterInfo(x, 16) for x in FP_REGS})

    disassembler = RiscVDisassembler(8, 16)
    lifter = RiscVLifter(8, 16)


class RiscV128(RiscV64):
    name = "riscv128"
    regs = {x: RegisterInfo(x, 16) for x in GP_REGS}

    disassembler = RiscVDisassembler(16)
    lifter = RiscVLifter(16)

class RiscV128F(RiscV128):
    name = "riscv128f"
    RiscV128.regs.update({x: RegisterInfo(x, 4) for x in FP_REGS})

    disassembler = RiscVDisassembler(16, 4)
    lifter = RiscVLifter(16, 4)

class RiscV128D(RiscV128):
    name = "riscv128d"
    RiscV128.regs.update({x: RegisterInfo(x, 8) for x in FP_REGS})

    disassembler = RiscVDisassembler(16, 8)
    lifter = RiscVLifter(16, 8)

class RiscV128Q(RiscV128):
    name = "riscv128q"
    RiscV128.regs.update({x: RegisterInfo(x, 16) for x in FP_REGS})

    disassembler = RiscVDisassembler(16, 16)
    lifter = RiscVLifter(16, 16)