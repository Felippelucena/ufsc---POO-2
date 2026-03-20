# Exercício 31

'''31. O Sr. Manoel Joaquim expandiu seus negócios para além dos negócios de 1,99 e agora 
possui uma loja de conveniências. Faça um programa que implemente uma caixa 
registradora rudimentar. O programa deverá receber um número desconhecido de valores 
referentes aos preços das mercadorias. Um valor zero deve ser informado pelo operador para
indicar o final da compra. O programa deve então mostrar o total da compra e perguntar o 
valor em dinheiro que o cliente forneceu, para então calcular e mostrar o valor do troco. 
Após esta operação, o programa deverá voltar ao ponto inicial, para registrar a próxima 
compra. A saída deve ser conforme o exemplo abaixo: 
Lojas Tabajara 
Produto 1: R$ 2.20
Produto 2: R$ 5.80
Produto 3: R$ 0
Total: R$ 9.00
Dinheiro: R$ 20.00
Troco: R$ 11.00
...'''


class CaixaRegistradora:
    def __init__(self):
        self.total_em_caixa = 0
        self.funcionando = True
        
        
    def iniciar(self):
        print('Caixa aberto')
        while self.funcionando:
            self.atender_cliente()
            self.funcionando = False if input('Aperte "f" para fechar o caixa, ou qualquer tecla para atender o proximo cliente:  ').lower() == "f" else True
        print(f'Valor total de entrada: {self.total_em_caixa}')
        print('Caixa Fechado')
            
            
        
    def atender_cliente(self):
        carrinho = []
        fim = 5
        while fim != 0:
            try:
                carrinho.append(float(input(f'Produto {len(carrinho)+1}: R$ ')))
                fim = carrinho[-1]
            except:
                print('Valor incorreto')
        carrinho.pop()
        print('Lojas Tabajara')
        for i, p in enumerate(carrinho): print(f'Produto {i+1}: R$ {p:.2f}')
        total = sum(carrinho)
        print(f'Total: R$ {total}')
        dinheiro_cliente = 0
        var = True
        while var:
            try:
                dinheiro_cliente = float(input(f'Dinheiro: R$ '))
                if dinheiro_cliente > total: var = False
                else: print('Dinheiro insuficiente')  
            except:
                print('Valor incorreto')
        print(f'Troco: R$ {(dinheiro_cliente-total):.2f}')
        self.total_em_caixa += total
            
        
    
caixa = CaixaRegistradora()

caixa.iniciar()