#Exercício 7
'''7. Faça um programa que leia 5 números e informe o maior número.'''

def maior_numero(lista):
    maior_numero = -10000000
    for num in lista:
        num = float(num)
        if num > maior_numero:
            maior_numero = num
    print(f'O maior numero é {maior_numero}')

if __name__ == '__main__':
    lista = [input(f"Digite o {x+1}º valor: ") for x in range(5)]
    print(lista)
    maior_numero(lista)
