#Exercício 6
'''6. Faça um programa que imprima na tela os números de 1 a 20, um abaixo do outro. Depois
modifique o programa para que ele mostre os números um ao lado do outro.'''

def valores_em_linha():
    for i in range(20):
        print(i+1)

def valores_em_coluna():
    linha = ''
    for x in range(20):
        linha+= (str(x+1) + ', ')
    linha = linha[:-2] + '.'
    print(linha)

if __name__ == '__main__':
    valores_em_linha()
    valores_em_coluna()
