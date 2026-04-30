#Exercício 18
'''18. Faça um programa que, dado um conjunto de N números, determine o menor valor, o 
maior valor e a soma dos valores. '''


def fatorial(n):
    if n <= 1: return 1
    return n * fatorial(n-1)


print(fatorial(5))