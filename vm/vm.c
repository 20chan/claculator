#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <math.h>
#include "opcodes.h"

#define STACK_SIZE 10

int stack[STACK_SIZE];
int stindex = 0;
int program_result = -1;

void push(int i) {
	stack[stindex++] = i;
}

int pop() {
	return stack[--stindex];
}

int top() {
	return stack[stindex - 1];
}

void handle();
FILE *f;
int main(int argc, char *argv[]) {
	if (argc < 2) {
		fprintf(stderr, "File name should be given as argument\n");
		return 1;
	}
	f = fopen(argv[1], "rb");
	fseek(f, 0, SEEK_END);
	long len = ftell(f);
	rewind(f);
	unsigned char buffer;
	while (fread(&buffer, (size_t)1, (size_t)1, f) == 1) {
	  handle(buffer);
	}
	fprintf(stdout, "result: %d\n", program_result);
	return 0;
}

void handle(int code) {
	fprintf(stdout, "code: %d, top: %d\n", code, top());
	if (code == PUSH_CONST_INT)	{
		unsigned char buffer[4];
		fread(&buffer, (size_t)4, (size_t)1, f);
		int param = *(int *) buffer;
		push(param);
		return;
	}
	if (code == PUSH_CONST_REAL) {
		
	}
	if (code >= BIN_ADD) {
		int left = pop();
		int right = pop();
		int res = 0;
		switch (code) {
			case BIN_ADD: res = left + right; break;
			case BIN_SUB: res = left - right; break;
			case BIN_MUL: res = left * right; break;
			case BIN_DIV: res = left / right; break;
			case BIN_MOD: res = left % right; break;
			case BIN_POW: res = pow(left, right); break;
		}
		push(res);
		return;
	}
	if (code == TERM_PLUS) return;
	if (code == TERM_MINUS) {
		push(-pop());
		return;
	}
	if (code == RET_VAL) {
		program_result = pop();
		return;
	}
}

void test_jit(void) {
	// mov eax, 0
	// add eax, 1
	// ret
	unsigned char code[] = { 0xb8, 0x00, 0x00, 0x00, 0x00, 0x83, 0xc0, 0x01, 0xc3 };

	int num = 42;
	memcpy(&code[1], &num, 4);
	void *mem = mmap(NULL, sizeof(code), PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
	memcpy(mem, code, sizeof(code));
	int(*func)() = mem;
	int res = func();
	fprintf(stdout, "%d\n", res);
}
