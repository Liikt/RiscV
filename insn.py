from binaryninja.log import log_warn
from binaryninja.enums import BranchType
from binaryninja.architecture import InstructionInfo
from binaryninja.function import InstructionTextToken as Token
from binaryninja.function import InstructionTextTokenType as TokenType

from enum import Enum
from struct import unpack


OPCODE_MASK = 0b1111111 <<  0
RD_MASK     = 0b11111   <<  7
FUNCT3_MASK = 0b111     << 12
RS1_MASK    = 0b11111   << 15
RS2_MASK    = 0b11111   << 20
FUNCT7_MASK = 0b1111111 << 25

GP_REGS = [
    "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1",
    "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
    "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6" 
]

r_type_opcodes = {
    0b0110011
}

i_type_opcodes = {
    0b1100111, 0b0000011, 0b0010011, 0b1110011, 0b0001111
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

    def get_text(self, _addr):
        pass

class RTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.RType

    mnemonics = {
        0b000: {
            0b0000000: "add",
            0b0100000: "sub",
        },
        0b001: {
            0b0000000: "sll",
        },
        0b010: {
            0b0000000: "slt",
        },
        0b011: {
            0b0000000: "sltu",
        },
        0b100: {
            0b0000000: "xor",
        },
        0b101: {
            0b0000000: "srl",
            0b0100000: "sra",
        },
        0b110: {
            0b0000000: "or",
        },
        0b111: {
            0b0000000: "and",
        },
    }

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

    def get_info(self, _addr):
        op  = Token(TokenType.InstructionToken, 
            self.mnemonics[self.funct3][self.funct7].ljust(8))
        space = Token(TokenType.TextToken, " ")
        sep = Token(TokenType.OperandSeparatorToken, ", ")
        rd  = Token(TokenType.RegisterToken, GP_REGS[self.rd])
        rs1 = Token(TokenType.RegisterToken, GP_REGS[self.rs1])
        rs2 = Token(TokenType.RegisterToken, GP_REGS[self.rs2])
        result = [
            op, space, rd, sep, rs1, sep, rs2
        ]
        return (result, self.length)

class ITypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.IType

    mnemonics = {
        0b0000011: {
            0b000: "lb",
            0b001: "lw",
            0b010: "lh",
            0b100: "lbu",
            0b101: "lhu",
        },
        0b0001111: {
            0b000: "fence",
        },
        0b0010011: {
            0b000:  "addi",
            0b001:  "slli",
            0b010:  "slti",
            0b011:  "sltiu",
            0b100:  "xori",
            0b101:  "srli",
            0b110:  "ori",
            0b111:  "andi",
            0b1101: "srai",
        },

    }

    def __init__(self, opcode, rd, rs1, funct3, imm, shmt):
        self.opcode = opcode
        self.rd  = rd
        self.rs1 = rs1
        self.funct3 = funct3
        self.imm = imm
        self.shmt = shmt

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

    def get_text(self, _addr):
        result = []
        space = Token(TokenType.TextToken, " ")
        sep = Token(TokenType.OperandSeparatorToken, ", ")
        rd  = Token(TokenType.RegisterToken, GP_REGS[self.rd])
        rs1 = Token(TokenType.RegisterToken, GP_REGS[self.rs1])

        if self.opcode in branch_instructions:
            if self.opcode == 0b1110011 and not self.imm:
                # ECALL
                result.append(Token(TokenType.InstructionToken, "ecall".ljust(8)))
            elif self.opcode == 0b1110011 and self.imm:
                # EBREAK
                result.append(Token(TokenType.InstructionToken, "ebreak".ljust(8)))
            elif self.opcode == 0b1100111:
                # JALR
                if self.rd:
                    tgt = (self.imm + self.rs1) & ((1 << 32) - 2)
                    result.append(Token(TokenType.InstructionToken, "jalr".ljust(8)))
                    result.append(space)
                    result.append(Token(TokenType.RegisterToken, GP_REGS[self.rd]))
                    result.append(sep)
                    result.append(Token(TokenType.IntegerToken, hex(self.imm), value=self.imm))
                    result.append(Token(TokenType.TextToken, "("))
                    result.append(Token(TokenType.RegisterToken, GP_REGS[self.rs1]))
                    result.append(Token(TokenType.TextToken, ")"))
                else:
                    result.append(Token(TokenType.InstructionToken, "ret"))

        elif self.opcode == 0b0000011:
            result.append(Token(TokenType.InstructionToken, self.mnemonics[self.opcode][self.funct3].ljust(8)))
            result.append(space)
            result.append(rd)
            result.append(sep)
            result.append(Token(TokenType.IntegerToken, hex(self.imm), value=self.imm))
            result.append(Token(TokenType.BeginMemoryOperandToken, "("))
            result.append(rs1)
            result.append(Token(TokenType.EndMemoryOperandToken, ")"))

        else:
            op = self.opcode
            if self.shmt is not None:
                op |= (self.imm >> 10) << 4

            mnemonic = self.mnemonics[op][self.funct3]
            if mnemonic == "addi" and self.rs1 == 0:
                mnemonic = "li"
            result.append(Token(TokenType.InstructionToken, mnemonic.ljust(8)))
            result.append(space)
            result.append(rd)
            if mnemonic != "li":
                result.append(sep)
                result.append(rs1)
            result.append(sep)
            val = self.imm if self.shmt is None else self.shmt
            result.append(Token(TokenType.IntegerToken, hex(val), value=val))

        return (result, self.length)

class STypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.SType

    mnemonics = {
        0b000: "sb",
        0b001: "sh",
        0b010: "sw",
    }

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

    def get_text(self, _addr):
        space = Token(TokenType.TextToken, " ")
        sep = Token(TokenType.OperandSeparatorToken, ", ")

        result = []
        result.append(Token(TokenType.InstructionToken, self.mnemonics[self.funct3].ljust(8)))
        result.append(space)
        result.append(Token(TokenType.RegisterToken, GP_REGS[self.rs2]))
        result.append(sep)
        result.append(Token(TokenType.IntegerToken, hex(self.imm), value=self.imm))
        result.append(Token(TokenType.BeginMemoryOperandToken, "("))
        result.append(Token(TokenType.RegisterToken, GP_REGS[self.rs1]))
        result.append(Token(TokenType.EndMemoryOperandToken, ")"))
        return (result, self.length)

class BTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.BType

    mnemonics = {
        0b000: "beq",
        0b001: "bne",
        0b100: "blt",
        0b101: "bge",
        0b110: "bltu",
        0b111: "bgeu",
    }

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

    def get_text(self, addr):
        space = Token(TokenType.TextToken, " ")
        sep = Token(TokenType.OperandSeparatorToken, ", ")

        result = []
        result.append(Token(TokenType.InstructionToken, self.mnemonics[self.funct3].ljust(8)))
        result.append(space)
        result.append(Token(TokenType.RegisterToken, GP_REGS[self.rs1]))
        result.append(sep)
        result.append(Token(TokenType.RegisterToken, GP_REGS[self.rs2]))
        result.append(sep)
        result.append(Token(TokenType.PossibleAddressToken, hex(self.imm + addr), value=self.imm + addr))
        return (result, self.length)


class UTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.UType

    mnemonics = {
        0b0110111: "lui",
        0b0010111: "auipc",
    }

    def __init__(self, opcode, rd, imm):
        self.opcode = opcode
        self.rd = rd
        self.imm = imm

    def get_info(self, _addr):
        info = super().get_info(_addr)
        info.length = self.length
        return info

    def get_text(self, _addr):
        space = Token(TokenType.TextToken, " ")
        sep = Token(TokenType.OperandSeparatorToken, ", ")

        result = []
        result.append(Token(TokenType.InstructionToken, self.mnemonics[self.opcode].ljust(8)))
        result.append(space)
        result.append(Token(TokenType.RegisterToken, GP_REGS[self.rd]))
        result.append(sep)
        result.append(Token(TokenType.IntegerToken, hex(self.imm), value=self.imm))
        return (result, self.length)

class JTypeInstruction(RiscVInstruction):
    length = 4
    insn_type = InstructionType.JType

    mnemonics = {
        0b1101111: "jal",
        0b11101111: "j",
    }

    def __init__(self, opcode, rd, imm):
        self.opcode = opcode
        self.rd = rd
        self.imm = imm

    def get_info(self, _addr):
        info = super().get_info(_addr)
        info.length = self.length
        info.add_branch(BranchType.CallDestination, target=self.imm)
        return info

    def get_text(self, addr):
        space = Token(TokenType.TextToken, " ")
        op = self.opcode | ((self.rd == 0) << 7)

        result = []
        result.append(Token(TokenType.InstructionToken, self.mnemonics[op].ljust(8)))
        result.append(space)
        if self.rd:
            result.append(Token(TokenType.RegisterToken, GP_REGS[self.rd]))
            result.append(Token(TokenType.TextToken, ", "))
        result.append(Token(TokenType.PossibleAddressToken, hex(self.imm + addr), value=self.imm + addr))
        return (result, self.length)


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

        shmt   = None
        imm    = (_get_funct7(insn) << 5) | _get_rs2(insn)
        if funct3 == 101:
            shmt = imm & 0b11111
        imm = _sign_extend(imm, 12)

        return ITypeInstruction(opcode, rd, rs1, funct3, imm, shmt)

    elif opcode in s_type_opcodes:
        rs1    = _get_rs1(insn)
        rs2    = _get_rs2(insn)
        funct3 = _get_funct3(insn)
        imm = (_get_funct7(insn) << 5) | _get_rd(insn)
        imm = _sign_extend(imm, 12)
        return STypeInstruction(opcode, rs1, rs2, funct3, imm)

    elif opcode in b_type_opcodes:
        imm_1 = _get_rd(insn)
        imm_2 = _get_funct7(insn)
        rs1    = _get_rs1(insn)
        rs2    = _get_rs2(insn)
        funct3 = _get_funct3(insn)
        imm = (((imm_2 >> 6)&1) << 12) | ((imm_1 & 1) << 11) | ((imm_2 & 0b111111) << 5) | (imm_1 & 0b11110)
        imm = _sign_extend(imm, 12)
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
        imm   = _sign_extend(imm, 20)

        rd = _get_rd(insn)
        return JTypeInstruction(opcode, rd, imm)

    else:
        log_warn(f"Wrong opcode 0b{opcode:07b} @ 0x{addr:08x}")
        return None