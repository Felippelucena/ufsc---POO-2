#Exercício 8
'''8. Faça um programa que leia 5 números e informe a soma e a média dos números.'''

def media_soma(array_numbers):
    soma = 0
    for num in array_numbers:
        soma += num
    media = soma/(len(array_numbers))
    print(f'soma: {soma}')
    print(f'media: {media}')
    
    
media_soma([1,2,3,4,5,6])
    
