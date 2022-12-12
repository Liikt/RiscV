func1:
    ret

_start:
    auipc   a0,0x8000
    lui     a5,0x8001
    jal     ra,func1
    j       test

next:
    jalr    ra,10(t0)
    beq     a4,a5,ebr
    bne     a4,a5,ec
    blt     a4,a5,label1
    bge     a4,a5,label1
    bltu    a4,a5,label1
    bgeu    a4,a5,label1
    lb      a4,160(a5)
    lh      a4,160(a5)
    lw      a4,160(a5)
    lbu     a5,0(a5)
    lhu     a5,0(a5)
    sb      a5,-21(s0)
    sh      s0,28(sp)
    sw      s0,28(sp)

label1:
    addi    sp,sp,-32
    li      a5,0
    mv      a0,a5
    slti    a0,a0,0x13
    sltiu   a0,a0,0x13
    xori    a0,a0,0x13
    ori     a0,a0,0x13
    andi    a0,a0,0x13
    slli    a0,a0,0x13
    srli    a0,a0,0x13
    srai    a0,a0,0x13
    add     t0,a1,sp
    sub     t0,a1,sp
    sll     t0,a1,sp
    slt     t0,a1,sp
    sltu    t0,a1,sp
    xor     t0,a1,sp
    srl     t0,a1,sp
    sra     t0,a1,sp
    or      t0,a1,sp
    and     t0,a1,sp
    j       next

ec:
    ecall

ebr:
    ebreak
