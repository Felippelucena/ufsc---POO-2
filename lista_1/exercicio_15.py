#Exercício 15
'''15. A série de Fibonacci é formada pela seqüência 1,1,2,3,5,8,13,21,34,55,... Faça um 
programa capaz de gerar a série até o n−ésimo termo.'''

def fibonacci_ate(n):
    fibonacci = [0, 1, 1]

    for _ in range(n-3):
        fibonacci.append(fibonacci[-2]+fibonacci[-1])

    print(fibonacci)
        
fibonacci_ate(15)
