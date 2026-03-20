#Exercício 29

'''29. O Sr. Manoel Joaquim possui uma grande loja de artigos de R$ 1,99, com cerca de 10 
caixas. Para agilizar o cálculo de quanto cada cliente deve pagar ele desenvolveu um tabela 
que contém o número de itens que o cliente comprou e ao lado o valor da conta. Desta forma
a atendente do caixa precisa apenas contar quantos itens o cliente está levando e olhar na 
tabela de preços. Você foi contratado para desenvolver o programa que monta esta tabela de 
preços, que conterá os preços de 1 até 50 produtos, conforme o exemplo abaixo: 
Lojas Quase Dois - Tabela de preços
1 - R$ 1.99
2 - R$ 3.98
...
50 - R$ 99.50'''

def tabela_de_precos(t, p, l):
    # t=tamanho da tabela, p=preço por unidade, l=loja.
    
    print(f'{l} - Tabela de preços')
    for i in range(t): print(f'{i+1} - R${((i+1)*p):.2f}')
    
tabela_de_precos(10, 1.99,'Lojas Quase Dois')

# Exercício 30

'''30. O Sr. Manoel Joaquim acaba de adquirir uma panificadora e pretende implantar a 
metodologia da tabelinha, que já é um sucesso na sua loja de 1,99. Você foi contratado para 
desenvolver o programa que monta a tabela de preços de pães, de 1 até 50 pães, a partir do 
preço do pão informado pelo usuário, conforme o exemplo abaixo: 
Preço do pão: R$ 0.18
Panificadora Pão de Ontem - Tabela de preços
1 - R$ 0.18
2 - R$ 0.36
...
50 - R$ 9.00
'''

tabela_de_precos(50, 0.18, 'Panificadora')

