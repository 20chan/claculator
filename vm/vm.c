#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

int main(int argc, char *argv[]) {
    // mov eax, 0
    // add eax, 1
    // ret
    unsigned char code[] = {0xb8, 0x00, 0x00, 0x00, 0x00, 0xfe, 0xc3};
    if (argc < 2) {
        fprintf(stderr, "Number should be given as argument");
        return 1;
    }

    int num = atoi(argv[1]);
    memcpy(&code[1], &num, 4);
    void *mem = mmap(NULL, sizeof(code), PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE, -1, 0);
    memcpy(mem, code, sizeof(code));
    int (*func)() = mem;
    return func();
}
