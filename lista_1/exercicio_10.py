#Exercício 10
'''10. Faça um programa que receba dois números inteiros e gere os números inteiros que estão
no intervalo compreendido por eles. '''

def valores_do_intervalo(num1,num2, ver_soma = False):
    menor = num1 if num1 < num2 else num2
    maior = num2 if num2 > num1 else num1
    valores = ''
    soma = 0
    for x in range(menor+1, maior):
        valores += (str(x) + ', ')
        soma += x
    valores = valores[:-2]+'.'
    print(valores)
    if ver_soma: print(soma)
    
valores_do_intervalo(30,20)
valores_do_intervalo(5,-12)
