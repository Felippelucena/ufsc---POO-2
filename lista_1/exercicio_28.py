#Exercício 28
'''28. Faça um programa que calcule o valor total investido por um colecionador em sua 
coleção de CDs e o valor médio gasto em cada um deles. O usuário deverá informar a 
quantidade de CDs e o valor para em cada um. '''

def media_soma(array_numbers):
    soma = 0
    for num in array_numbers:
        soma += num
    media = soma/(len(array_numbers))
    return [media, soma]

def investimento_da_colecao():
    try:
        n_turmas = int(input('Número de Cds: '))
        n_alunos = []
        for i in range(n_turmas):
            n = 50
            while n > 40:
                n = int(input(f'Valor gasto no {i+1}º cd: '))
            n_alunos.append(n)
        media = media_soma(n_alunos)[0]
        soma = media_soma(n_alunos)[1]
        print(f'Valor médio por cd: {media}, total gasto pela coleção: {soma}')
        
    except:
        pass
    
investimento_da_colecao()