from datetime import datetime
from compiler import compile2bytes
from interpreter import execute
from machine import run

def timeelapse(func):
    def wrapper(*args):
        before = datetime.now()
        func(*args)
        after = datetime.now()
        print(f'Time elapsed : {(after - before).microseconds}')
    return wrapper

@timeelapse
def run_interpreter(code):
    print(f'Interpreted : {execute(code)}')

@timeelapse
def run_compiler(code):
    print(f'Compiled    : {run(compile2bytes(code))}')

while True:
    print('=>', end=' ')
    expr = input()
    run_interpreter(expr)
    run_compiler(expr)
