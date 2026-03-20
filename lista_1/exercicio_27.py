#Exercício 27
'''27. Faça um programa que calcule o número médio de alunos por turma. Para isto, peça a 
quantidade de turmas e a quantidade de alunos para cada turma. As turmas não podem ter 
mais de 40 alunos. '''

def media_soma(array_numbers):
    soma = 0
    for num in array_numbers:
        soma += num
    media = soma/(len(array_numbers))
    return media

def media_alunos():
    try:
        n_turmas = int(input('Número de turmas: '))
        n_alunos = []
        for i in range(n_turmas):
            n = 50
            while n > 40:
                n = int(input(f'Quantidade de alunos na turma {i+1}: '))
            n_alunos.append(n)
        media = media_soma(n_alunos)
        print(f'Media de alunos por turma: {media}')
        
    except:
        pass
    
media_alunos()