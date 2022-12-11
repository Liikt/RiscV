from binaryninja.log import log_warn
from binaryninja.enums import BranchType
from binaryninja.architecture import InstructionInfo

from enum import Enum
from struct import unpack


OPCODE_MASK = 0b1111111 <<  0
RD_MASK     = 0b11111   <<  7
FUNCT3_MASK = 0b111     << 12
RS1_MASK    = 0b11111   << 15
RS2_MASK    = 0b11111   << 20
FUNCT7_MASK = 0b1111111 << 25

r_type_opcodes = {
    0b0110011
}

i_type_opcodes = {
    0b1100111, 0b0000011, 0b0010011, 0b1110011, 0b0001111, 0b1110011
}

s_type_opcodes = {
    0b0100011
}

b_type_opcodes = {
    0b1100011
}

u_type_opcodes = {
    0b0110111, 0b0010111
}

j_type_opcodes = {
    0b1101111
}

branch_instructions = {
    0b1101111, 0b1100111, 0b1100011, 0b1110011
}


def _get_opcode(insn):
    return insn & OPCODE_MASK

def _get_rd(insn):
    return (insn & RD_MASK) >> 7

def _get_funct3(insn):
    return (insn & FUNCT3_MASK) >> 12

def _get_rs1(insn):
    return (insn & RS1_MASK) >> 15

def _get_rs2(insn):
    return (insn & RS2_MASK) >> 20

def _get_funct7(insn):
    return (insn & FUNCT7_MASK) >> 25

def _get_big_imm(insn):
    return insn >> 12

def _sign_extend(x, b):
    m = 1 << (b - 1)
    x = x & ((1 << b) - 1)
    return (x ^ m) - m


class InstructionType(Enum):
    NoType = -1,
    RType  =  0,
    IType  =  1,
    SType  =  2,
    BType  =  3,
    UType  =  4,
    JType  =  5,

class RiscVInstruction(object):
    length = 0
    opcode = 0
    insn_type = InstructionType.NoType

    def __init__(self):
        pass

    def get_info(self, _addr):
        return InstructionInfo()

    def get_text(self):
        pass

class RTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.RType

    def __init__(self, opcode, rd, rs1, rs2, funct3, funct7):
        self.opcode = opcode
        self.rd  = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.funct3 = funct3
        self.funct7 = funct7

    def get_info(self, _addr):
        info = super().get_info(_addr)
        info.length = self.length
        return info

class ITypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.IType

    def __init__(self, opcode, rd, rs1, funct3, imm):
        self.opcode = opcode
        self.rd  = rd
        self.rs1 = rs1
        self.funct3 = funct3
        self.imm = imm

    def get_info(self, _addr):
        info = super().get_info(_addr)
        info.length = self.length

        if self.opcode in branch_instructions:
            if self.opcode == 0b1110011 and not self.imm:
                # ECALL
                info.add_branch(BranchType.SystemCall)
            elif self.opcode == 0b1110011 and self.imm:
                # EBREAK
                info.add_branch(BranchType.ExceptionBranch)
            elif self.opcode == 0b1100111:
                # JALR
                info.add_branch(BranchType.IndirectBranch)

        return info

class STypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.SType

    def __init__(self, opcode, rs1, rs2, funct3, imm):
        self.opcode = opcode
        self.rs1 = rs1
        self.rs2 = rs2
        self.funct3 = funct3
        self.imm = imm

    def get_info(self, _addr):
        info = super().get_info(_addr)
        info.length = self.length
        return info

class BTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.BType

    def __init__(self, opcode, rs1, rs2, funct3, imm):
        self.opcode = opcode
        self.rs1 = rs1
        self.rs2 = rs2
        self.funct3 = funct3
        self.imm = imm

    def get_info(self, addr):
        info = super().get_info(addr)
        info.length = self.length
        info.add_branch(BranchType.TrueBranch,  target=addr + self.imm)
        info.add_branch(BranchType.FalseBranch, target=addr + 4)
        return info


class UTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.UType

    def __init__(self, opcode, rd, imm):
        self.opcode = opcode
        self.rd = rd
        self.imm = imm

    def get_info(self, _addr):
        info = super().get_info(_addr)
        info.length = self.length
        return info

class JTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.JType

    def __init__(self, opcode, rd, imm):
        self.opcode = opcode
        self.rd = rd
        self.imm = imm

    def get_info(self, _addr):
        info = super().get_info(_addr)
        info.length = self.length
        info.add_branch(BranchType.CallDestination, target=self.imm)
        return info

def from_bytes(insn_bytes, addr):
    if len(insn_bytes) != 4 or addr % 4 != 0:
        return None
    insn = unpack("<I", insn_bytes)[0]
    opcode = _get_opcode(insn)

    if opcode in r_type_opcodes:
        rd  = _get_rd(insn)
        rs1 = _get_rs1(insn)
        rs2 = _get_rs2(insn)
        funct3 = _get_funct3(insn)
        funct7 = _get_funct7(insn)
        return RTypeInstruction(opcode, rd, rs1, rs2, funct3, funct7)

    elif opcode in i_type_opcodes:
        rd     = _get_rd(insn)
        rs1    = _get_rs1(insn)
        funct3 = _get_funct3(insn)
        imm    = (_get_funct7(insn) << 5) | _get_rs2(insn)
        return ITypeInstruction(opcode, rd, rs1, funct3, imm)

    elif opcode in s_type_opcodes:
        imm = (_get_funct7(insn) << 5) | _get_rd(insn)
        rs1    = _get_rs1(insn)
        rs2    = _get_rs2(insn)
        funct3 = _get_funct3(insn)
        return STypeInstruction(opcode, rs1, rs2, funct3, imm)

    elif opcode in b_type_opcodes:
        imm_1 = _get_rd(insn)
        imm_2 = _get_funct7(insn)
        rs1    = _get_rs1(insn)
        rs2    = _get_rs2(insn)
        funct3 = _get_funct3(insn)
        imm = ((imm_2 >> 6) << 12) | ((imm_1 & 1) << 11) | ((0b111111 & imm_2) << 5) | ((0b11110 & imm_1) << 1)
        imm = _sign_extend(imm << 19, 32) >> 19
        return BTypeInstruction(opcode, rs1, rs2, funct3, imm)

    elif opcode in u_type_opcodes:
        imm = _get_big_imm(insn) << 12
        rd = _get_rd(insn)
        return UTypeInstruction(opcode, rd, imm)

    elif opcode in j_type_opcodes:
        imm_parts = _get_big_imm(insn)

        imm_1 =  imm_parts        & 0b11111111
        imm_2 = (imm_parts >> 8)  & 0b1
        imm_3 = (imm_parts >> 9)  & 0b1111111111
        imm_4 = (imm_parts >> 19) & 0b1
        imm   = (imm_4 << 20) | (imm_1 << 12) | (imm_2 << 11) | (imm_3 << 1)
        imm   = _sign_extend(imm << 11, 32) >> 11

        rd = _get_rd(insn)
        return JTypeInstruction(opcode, rd, imm)

    else:
        log_warn(f"Wrong opcode 0b{opcode:07b} @ 0x{addr:08x}")
        return None