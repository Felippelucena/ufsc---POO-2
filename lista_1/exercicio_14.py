#Exercício 14
'''14. Faça um programa que peça 10 números inteiros, calcule e mostre a quantidade de 
números pares e a quantidade de números impares. '''

def quant_par_impar(lista):
    try:
        par = 0
        impar = 0
        for num in lista:
            num = int(num)
            par += 1 if num%2==0 else 0
            impar += 1 if num%2==1 else 0
        print(f'numero de pares: {par}')
        print(f'numero de ímpares: {impar}')
    except:
        print('Entrada incorreta, digite apenas numeros inteiros')
        
quant_par_impar([33,25,75,354,214,565,15,423,15,42,16,547,456])
quant_par_impar([input(f'Digite o {x+1}º valor da lista') for x in range(10)])
