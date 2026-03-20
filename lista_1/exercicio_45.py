# Exercício 45

'''45. Em uma eleição presidencial existem quatro candidatos. Os votos são informados por 
meio de código. Os códigos utilizados são: 
1 , 2, 3, 4  - Votos para os respectivos candidatos 
(você deve montar a tabela ex: 1 - Jose/ 2- João/etc)
5 - Voto Nulo
6 - Voto em Branco
Faça um programa que calcule e mostre: 
• O total de votos para cada candidato; 
• O total de votos nulos; 
• O total de votos em branco; 
• A percentagem de votos nulos sobre o total de votos; 
• A percentagem de votos em branco sobre o total de votos. Para finalizar o conjunto de votos 
tem-se o valor zero.  '''

opcoes_de_votos = ['Encerrar Votação', 'Jose', 'João', 'Maria', 'Ana', 'Nulo', 'Branco']

dados = [0,0,0,0,0,0,0]

def urna():
    voto = 1
    opcoes = 'Opções: '
    for c, v in enumerate(opcoes_de_votos): opcoes += f'Digite {c} para: {v}; '
    print(opcoes)
    while voto != 0:
        try:
            voto = int(input('Digite seu voto: '))
            if voto > 0 and voto < 7:  dados[voto] += 1
            elif voto != 0: print('Entrada incorreta')
        except:
            print('Entrada incorreta')

def eleicao():
    print('começando as eleicoes')
    urna()
    print('Resultados:')
    for i, opcao in enumerate(opcoes_de_votos[2:]): print(f'Total de votos para {opcao}: {dados[i]}')
    print(f'Percentagem de votos nulos sobre o total de votos: {dados[5]/sum(dados)*100:.2f}%')
    print(f'Percentagem de votos em branco sobre o total de votos: {dados[6]/sum(dados)*100:.2f}%')

eleicao()