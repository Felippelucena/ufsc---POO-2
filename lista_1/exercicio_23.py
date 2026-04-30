#Exercício 23
'''Números primos
- Criar uma função em sua linguagem preferida. A função deve receber um número N > 1 (validar o input), e retornar todos os números primos até o número N. EX. p(2) = [2]; p(3) = [2, 3]; p(10) = [2, 3, 5, 7];

--- Criar uma função recursiva que resolva p
--- Criar uma função linear que resolva p'''

def primos(n):
    if n < 2:
        return []
    primos = []
    for i in range(2, n + 1):
        primo = True
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                primo = False
                break
        if primo:
            primos.append(i)
    return primos

print(primos(10))

def primos_recursivo(n, i=2, primos=[]):
    if n < 2:
        return []
    if i > n:
        return primos
    primo = True
    for j in range(2, int(i**0.5) + 1):
        if i % j == 0:
            primo = False
            break
    if primo:
        primos.append(i)
    return primos_recursivo(n, i + 1, primos)