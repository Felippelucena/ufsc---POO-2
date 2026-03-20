#Exercício 9
'''9. Faça um programa que imprima na tela apenas os números ímpares entre 1 e 50. '''

def valores_impares(inicio, fim, espaco):
    linha = ''
    for x in range(inicio, fim, espaco):
        linha+= (str(x+1) + ', ')
        
    linha = linha[:-2] + '.'
    
    print(linha)
    
valores_impares(0, 50, 2)
