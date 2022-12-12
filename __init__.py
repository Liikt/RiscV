import binaryninja as bn
from .riscv import *
from .calling_conventions import RiscVWithFloats, RiscVWithoutFloats

variants = [
    (RiscV32, "riscv32"), (RiscV32F, "riscv32f"), (RiscV32D, "riscv32d"), (RiscV32Q, "riscv32q"),
    (RiscV64, "riscv64"), (RiscV64F, "riscv64f"), (RiscV64D, "riscv64d"), (RiscV64Q, "riscv64q"),
    (RiscV128, "riscv128"), (RiscV128F, "riscv128f"), (RiscV128D, "riscv128d"), (RiscV128Q, "riscv128q"),
]

DEFAULT_VARIANT = "riscv32"

for (Risc, name) in variants:
    Risc.register()
    riscv = bn.architecture.Architecture[name]
    if name[-1] not in ["f", "d", "q"]:
        riscv.register_calling_convention(RiscVWithoutFloats(riscv, 'default'))
    else:
        riscv.register_calling_convention(RiscVWithFloats(riscv, 'default'))
    riscv.standalone_platform.default_calling_convention = riscv.calling_conventions['default']

    if name == DEFAULT_VARIANT:
        bn.binaryview.BinaryViewType['ELF'].register_arch(
            243, bn.enums.Endianness.LittleEndian, riscv
        )