from exercicio_04 import calcularTaxadeCrescimento

#Exercício 5
'''5. Altere o programa anterior permitindo ao usuário informar as populações e as taxas de 
crescimento iniciais. Valide a entrada e permita repetir a operação. '''


if __name__ == '__main__':
    
    paisA = {
        'habitantes': input('Digite o valor da população do país A: '),
        'crescimento_por_ano': input('Digite a taxa de crescimento do país A em fração: ')
    }

    paisB = {
        'habitantes': input('Digite o valor da população do país B: '),
        'crescimento_por_ano': input('Digite a taxa de crescimento do país B em fração: ')
    }
    
    calcularTaxadeCrescimento(paisA, paisB)
