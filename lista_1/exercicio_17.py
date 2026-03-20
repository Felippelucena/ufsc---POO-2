#Exercício 17
'''17. Faça um programa que calcule o fatorial de um número inteiro fornecido pelo usuário. 
Ex.: 5!=5.4.3.2.1=120 '''

def fatorial(num):
    try:
        num = int(num)
        if num == 0: return 1
        return num * fatorial(num-1)
    except: print('Entrada incorreta, deve ser um numero inteiro')
    
    
fatorial(input('Digite um numero inteiro'))
