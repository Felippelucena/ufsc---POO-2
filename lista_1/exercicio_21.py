#Exercício 21
'''21. Faça um programa que peça um número inteiro e determine se ele é ou não um número 
primo. Um número primo é aquele que é divisível somente por ele mesmo e por 1. '''

#Exercício 22
'''22. Altere o programa de cálculo dos números primos, informando, caso o número não seja 
primo, por quais número ele é divisível. '''

def divide(n):
    divisores = []
    for x in range(1,n):
        if n%x==0: divisores.append(x)
    return f'divisores: {divisores}'

def e_primo(n):
    if n < 2: return False
    for x in range(2,n-2):
        if n%x==0: return divide(n)
    return True
        
print(e_primo(88))
print(e_primo(47))
