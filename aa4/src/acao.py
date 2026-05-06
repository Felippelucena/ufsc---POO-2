'''
Hierarquia de Ações de um jogador em uma rodada de apostas.

Classe base: Acao
Subclasses concretas: Passar, Pagar, Aumentar, Desistir, AllIn

Cada subclasse implementa executar(jogador, mesa), aplicando o efeito da ação.
O Dealer chama acao.executar(...) sem saber qual subclasse — polimorfismo.
'''


class Acao:
    nome = 'acao'

    def executar(self, jogador, mesa):
        raise NotImplementedError("Subclasses devem implementar executar.")

    def __str__(self):
        return self.nome


class Passar(Acao):
    nome = 'passar'

    def executar(self, jogador, mesa):
        return 0


class Desistir(Acao):
    nome = 'desistir'

    def executar(self, jogador, mesa):
        jogador.desistir()
        return 0


class Pagar(Acao):
    nome = 'pagar'

    def executar(self, jogador, mesa):
        diff = mesa.aposta_atual - jogador.aposta_rodada
        return mesa.receber_aposta(jogador, diff)


class Aumentar(Acao):
    nome = 'aumentar'

    def __init__(self, valor):
        valor = int(valor)
        if valor <= 0:
            raise ValueError("Valor de aumento deve ser positivo.")
        self.valor = valor

    def executar(self, jogador, mesa):
        return mesa.receber_aposta(jogador, self.valor)

    def __str__(self):
        return f"aumentar {self.valor}"


class AllIn(Acao):
    nome = 'all_in'

    def executar(self, jogador, mesa):
        return mesa.receber_aposta(jogador, jogador.fichas)
