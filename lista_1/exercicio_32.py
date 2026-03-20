# Exercício 32

''''32. Faça um programa que calcule o fatorial de um número inteiro fornecido pelo usuário. 
Ex.: 5!=5.4.3.2.1=120. A saída deve ser conforme o exemplo abaixo: 
Fatorial de: 5
5! =  5 . 4 . 3 . 2 . 1 = 120'''

def f(n):
    if n == 1: return 1
    return n * f(n-1)


def fatorial(n):
    result = f(n)
    print(f'Fatorial de: {n}')
    text = f'{n}! = '
    for i in range(n-1): text += f'{n-i} . '
    text += f'1 = {result}'
    print(text)

fatorial(8)