#Exercício 4
'''4. Supondo que a população de um país A seja da ordem de 80000 habitantes com uma taxa 
anual de crescimento de 3% e que a população de B seja 200000 habitantes com uma taxa 
de crescimento de 1.5%. Faça um programa que calcule e escreva o número de anos 
necessários para que a população do país A ultrapasse ou iguale a população do país B, 
mantidas as taxas de crescimento.'''

paisA = {
    'habitantes': 80000,
    'crescimento_por_ano': 0.03
}

paisB = {
    'habitantes': 200000,
    'crescimento_por_ano': 0.015
}

def calcularTaxadeCrescimento(paisA, paisB):
    anos = 0
    habitantesA = int(paisA['habitantes'])
    habitantesB = int(paisB['habitantes'])
    while habitantesA < habitantesB:
        habitantesA += int(habitantesA*float(paisA['crescimento_por_ano']))
        habitantesB += int(habitantesB*float(paisB['crescimento_por_ano']))
        anos += 1

    print(f'Demorou {anos} anos para o país A ficar com {habitantesA} habitantes e o país B ficar com {habitantesB} habitantes')

if __name__ == '__main__':
    calcularTaxadeCrescimento(paisA, paisB)
