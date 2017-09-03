from interpreter import execute

while True:
    print('=>', end=' ')
    print(execute(input()))
