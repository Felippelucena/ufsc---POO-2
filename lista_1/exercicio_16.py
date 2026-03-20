#Exercício 16
'''16. A série de Fibonacci é formada pela seqüência 0,1,1,2,3,5,8,13,21,34,55,... Faça um 
programa que gere a série até que o valor seja maior que 500.'''

def fibonacci_ate(n):
    fibonacci = [0, 1, 1]
    while fibonacci[-1] < n: 
        fibonacci.append(fibonacci[-1]+fibonacci[-2])

    print(fibonacci)
        
fibonacci_ate(500)
