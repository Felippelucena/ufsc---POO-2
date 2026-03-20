#Exercício 25
'''25. Faça um programa que peça para n pessoas a sua idade, ao final o programa devera 
verificar se a média de idade da turma varia entre 0 e 25,26 e 60 e maior que 60; e então, 
dizer se a turma é jovem, adulta ou idosa, conforme a média calculada.'''

def media_idade(n_alunos):
    data = {
            'jovem' : 0,
            'adulta' : 0,
            'idosa' : 0
        }
    
    def registrar_idade(n):
        if n < 26: data['jovem'] += 1
        elif n < 61: data['adulta'] += 1
        else: data['idosa'] +=1
        
    try:
        n_alunos = int(n_alunos)
        idade_alunos = [input(f'Digite a idade do {x+1}º aluno: ') for x in range(n_alunos)]
        
        soma = 0
        for idade_aluno in idade_alunos:
            n = int(idade_aluno)
            soma += n
            registrar_idade(n)
        media = soma/ len(idade_alunos)
        registrar_idade(media)
        turma_e = ''
        maior = -1
        for key, value in data.items():
            if value > maior:
                maior = value
                turma_e = key
        
        print(f'A turma é {turma_e} e a idade é média é {media}')
            
    except:
        print('Entrada incorreta, é espérado uma lista de numero inteiros')
        
        
if __name__ == '__main__':
    n_alunos = input('Quandos alunos na turma: ')
    
    media_idade(n_alunos)
    
    
        
