#Exercício 26
'''26. Numa eleição existem três candidatos. Faça um programa que peça o número total de 
eleitores. Peça para cada eleitor votar e ao final mostrar o número de votos de cada 
candidato. '''

canditatos = {
    1: 0,
    2: 0,
    3: 0
}



def urna_eletronica(voto):
    try:
        voto = int(voto)
        if voto in canditatos:
            canditatos[voto] += 1
        else:
            urna_eletronica(input('Voto invalido, tente novamente: '))
            
    except: urna_eletronica(input('Voto invalido, tente novamente: '))
    
def eleicao():
    n_eleitores = input('Digite o numero de eleitores: ')
    try:
        n_eleitores = int(n_eleitores)
        for x in range(n_eleitores):
            voto = input(f'Eleitor {x+1}, digite seu voto: ')

            urna_eletronica(voto)

    except:
        print('Entrada invalida, é esperado um numero inteiro')
    
    print(f'Canditado 1: {canditatos[1]} votos')
    print(f'Canditado 2: {canditatos[2]} votos')
    print(f'Canditado 3: {canditatos[3]} votos')
        
if __name__ == '__main__':
    eleicao()