OUTPUT_ARCH("riscv")

MEMORY
{
    itim  : ORIGIN = 0x08000000, LENGTH = 8K
}

SECTIONS
{
    .text : {
        . += 4K;
        *(.text)
    } > itim

    .data : {
        *(.data)
    } > itim

    .rodata : {
        *(.rodata)
    } > itim

    .bss : {
        *(.bss)
    } > itim

    /DISCARD/ : {
        *(.comment)
        *(.riscv.attributes)
        *(.rela.*)
    }
}