AS=riscv64-unknown-elf-as

TARGETS=tests/rv32i.bin

all: $(TARGETS)

tests/%.bin: tests/%.S
	$(AS) -c $< -o $@