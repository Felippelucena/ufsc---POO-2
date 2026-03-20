#Exercício 13
'''13. Faça um programa que peça dois números, base e expoente, calcule e mostre o primeiro 
número elevado ao segundo número. Não utilize a função de potência da linguagem. '''

def calcular_potencia(base, expoente):
    resultado = 1
    for _ in range(expoente): resultado *= base
    
    if expoente == 2: print(f'{base} elevado ao quadrado é igual a {resultado}')
    elif expoente == 3: print(f'{base} elevado ao cubo é igual a {resultado}')
    else: print(f'{base} elevado a {expoente} é igual a {resultado}')
    
calcular_potencia(7,5)
calcular_potencia(4,2)
calcular_potencia(2,3)
