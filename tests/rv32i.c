int foo(int a, int b, char c) {
    switch (c)
    {
    case '+':
        return a+b;
    case '-':
        return a-b;
    case '<':
        return a<<b;
    case '>':
        return a>>b;
    default:
        return 0x13371337;
    }
}

int main(int argc, char **argv) {
    int a = foo(20, 10, '+');
    int b = foo(10, 20, '-');

    if (a != b && (unsigned int)a < (unsigned int)b) {
        return foo(a, b, '<');
    }
    if (a != b && (unsigned int)a > (unsigned int)b) {
        asm("ecall");
        return 1;
    }
    asm("ebreak");
}