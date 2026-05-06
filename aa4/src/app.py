from datetime import datetime
from src.mesa import Mesa
from src.dealer import Dealer
from src.jogador import criar_jogador
from src.bancoDeDados import BancoDeDados

'''
Classe App
Orquestra a partida: cria mesa/dealer/jogadores, conduz o loop até sobrar 1
jogador com fichas, registra a vitória no ranking.

Métodos:
configurar_partida(...): Monta mesa, jogadores e dealer.
jogar_partida(): Loop de mãos até a sessão acabar; retorna resumo.
registrar_vitoria(resumo): Persiste no ranking.
listar_ranking(): Retorna ranking via BancoDeDados.
'''


class App:
    def __init__(self):
        self.__mesa = None
        self.__dealer = None
        self.__ranking = BancoDeDados.carregar_dados('ranking') or []

    @property
    def mesa(self):
        return self.__mesa

    @property
    def dealer(self):
        return self.__dealer

    @property
    def ranking(self):
        return list(self.__ranking)

    def configurar_partida(self, nome_humano, n_ias, fichas_iniciais=1000, sb=10, bb=20):
        if not (1 <= n_ias <= 3):
            raise ValueError("Número de IAs deve ser entre 1 e 3.")
        self.__mesa = Mesa(small_blind=sb, big_blind=bb)
        humano = criar_jogador(tipo='humano', nome=nome_humano, fichas=fichas_iniciais)
        self.__mesa.adicionar_jogador(humano)
        nomes_ia = ['Bot Alice', 'Bot Bruno', 'Bot Clara']
        for i in range(n_ias):
            ia = criar_jogador(tipo='ia', nome=nomes_ia[i], fichas=fichas_iniciais)
            self.__mesa.adicionar_jogador(ia)
        self.__dealer = Dealer(self.__mesa)

    def jogar_partida(self):
        if not self.__mesa or not self.__dealer:
            raise ValueError("Configure a partida antes de jogar.")

        n_inicial = len(self.__mesa.jogadores)

        while len(self.__mesa.jogadores_com_fichas()) >= 2:
            self.__dealer.iniciar_partida()

            go = self.__dealer.executar_rodada_apostas()
            while go and self.__dealer.estado != 'showdown':
                self.__dealer.avancar_estado()
                if self.__dealer.estado == 'showdown':
                    break
                go = self.__dealer.executar_rodada_apostas()

            self.__dealer.encerrar_partida()
            self.__mesa.avancar_dealer()

        com_fichas = self.__mesa.jogadores_com_fichas()
        if com_fichas:
            vencedor = max(com_fichas, key=lambda j: j.fichas)
        else:
            vencedor = max(self.__mesa.jogadores, key=lambda j: j.fichas)

        resumo = {
            "vencedor": vencedor.nome,
            "fichas_finais": vencedor.fichas,
            "n_jogadores": n_inicial,
            "data": datetime.now().strftime('%d/%m/%Y %H:%M'),
        }
        self.registrar_vitoria(resumo)
        return resumo

    def registrar_vitoria(self, resumo: dict):
        BancoDeDados.registrar_vitoria(resumo)
        self.__ranking = BancoDeDados.carregar_dados('ranking') or []

    def listar_ranking(self, top=10):
        return BancoDeDados.listar_ranking(top=top)
