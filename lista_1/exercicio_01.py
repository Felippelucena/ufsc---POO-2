#Exercício 1
'''1. Faça um programa que peça uma nota, entre zero e dez. Mostre uma mensagem caso o 
valor seja inválido e continue pedindo até que o usuário informe um valor válido. '''

def cadastrarNota (x):
    is_valid = False
    while is_valid == False:
        try:
            x = int(x)
            if x >= 0 and x <= 10:
                is_valid = True
            else:
                x = input('Valor invalido, digite uma nota de 0 a 10: ')
        except:

            x = input('Valor invalido, digite uma nota de 0 a 10: ')
    print(f'Nota {x} cadastrada com sucesso!')

if __name__ == '__main__':
    cadastrarNota(input('Digite uma nota de 0 a 10: '))
