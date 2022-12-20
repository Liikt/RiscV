CC = riscv64-unknown-elf-gcc
AS = riscv64-unknown-elf-as
LD = riscv64-unknown-elf-ld
OBJCOPY = riscv64-unknown-elf-objcopy
OBJDUMP = riscv64-unknown-elf-objdump

OBJ = rv32i.o

CFLAGS = -march=rv32i -mabi=ilp32 -mstrict-align -Wno-builtin-declaration-mismatch -O0
LDFLAGS = -Trv32i.lds -m elf32lriscv
OFLAGS = -O binary -j .text -j .data -j .rodata -j .bss

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<

%.o: %.S
	$(AS) $(CFLAGS) -o $@ -c $<

rv32i: $(OBJ)
	$(LD) -o $@ $(OBJ) $(LDFLAGS)
	$(OBJCOPY) $(OFLAGS) $@ $@.tmp
	dd if=$@.tmp of=$@.bin bs=1 skip=4096

objdump: rv32i 
	$(OBJDUMP) -D $<

clean:
	rm rv32i rv32i.o rv32i.bin rv32i.tmp || true

