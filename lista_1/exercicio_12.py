#Exercício 12
'''12. Desenvolva um gerador de tabuada, capaz de gerar a tabuada de qualquer número inteiro
entre 1 a 10. O usuário deve informar de qual numero ele deseja ver a tabuada. A saída deve 
ser conforme o exemplo abaixo: 
Tabuada de 5:
5 X 1 = 5
5 X 2 = 10
...
5 X 10 = 50'''

def ver_tabuada_do(num):
    print(f'Tabuada do {num}:')
    for x in range(10):
        print(f'{num} X {x+1} = {num*(x+1)}')
        
ver_tabuada_do(9)
