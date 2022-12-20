from binaryninja.log import log_debug

from .variants.rv32 import from_bytes as from_bytes_rv32


def from_bytes(data, addr, xlen, flen):
    ret = None
    if ret is None and xlen == 4:
        ret = from_bytes_rv32(data, addr)
    
    if ret is None:
        log_debug(f"Wrong Instruction {data} @ {addr:08x}")

    return ret

