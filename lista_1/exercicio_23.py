#Exercício 23
'''23. Faça um programa que mostre todos os primos entre 1 e N sendo N um número inteiro 
fornecido pelo usuário. O programa deverá mostrar também o número de divisões que ele 
executou para encontrar os números primos. Serão avaliados o funcionamento, o estilo e o 
número de testes (divisões) executados. '''

def primos_entre_1_e_(n):
    log = {
        'divisoes': 0,
        'divisiveis': 0,
        'primos' : [2,3],
        
    }
    for x in range(3, n+1):
        for y in range(2, x-1):
            log['divisoes'] += 1
            if x%y==0: 
                log['divisiveis'] += 1
                break
            if y == x-2 : log['primos'].append(x)
    log['n_primos'] = len(log['primos'])
    return log

print(primos_entre_1_e_(100))
