import os
from src.mesa import Mesa
from src.avaliadorMao import AvaliadorMao
from src.acao import Acao


def _limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def _tela_publica(titulo, linhas):
    _limpar_tela()
    print(f"\n=== {titulo} ===")
    for linha in linhas:
        print(linha)
    input("\n  (Enter para continuar) ")
    _limpar_tela()

'''
Classe Dealer
Compõe Mesa. Controla o fluxo da partida via máquina de estados.

Estados: 'aguardando', 'pre_flop', 'flop', 'turn', 'river', 'showdown', 'encerrada'.

Métodos:
iniciar_partida(), cobrar_blinds(), distribuir_cartas_privadas(),
avancar_estado(), executar_rodada_apostas(), executar_showdown(), encerrar_partida().
'''


ESTADOS = ('aguardando', 'pre_flop', 'flop', 'turn', 'river', 'showdown', 'encerrada')


class Dealer:
    def __init__(self, mesa):
        if not isinstance(mesa, Mesa):
            raise ValueError("Dealer requer uma Mesa.")
        self.__mesa = mesa
        self.__estado = 'aguardando'

    @property
    def mesa(self):
        return self.__mesa

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        if value not in ESTADOS:
            raise ValueError(f"Estado inválido. Deve ser um de: {', '.join(ESTADOS)}.")
        self.__estado = value

    def iniciar_partida(self):
        self.__mesa.resetar_para_nova_partida()
        self.cobrar_blinds()
        self.distribuir_cartas_privadas()
        self.estado = 'pre_flop'
        dealer_nome = self.__mesa.jogadores[self.__mesa.indice_dealer].nome
        ordem_jogadores = ', '.join(j.nome for j in self.__mesa.jogadores if j.estado == 'ativo')
        _tela_publica(
            "NOVA MÃO",
            [
                f"  Dealer: {dealer_nome}",
                f"  Jogadores em jogo: {ordem_jogadores}",
                f"  Pote inicial (blinds): {self.__mesa.pote.total}",
            ],
        )

    def cobrar_blinds(self):
        jogadores = self.__mesa.jogadores
        n = len(jogadores)
        vivos = [j for j in jogadores if j.estado == 'ativo']
        if len(vivos) < 2:
            raise ValueError("Mesa precisa de pelo menos 2 jogadores ativos.")
        idx_d = self.__mesa.indice_dealer

        def proximo_ativo(idx):
            for k in range(1, n + 1):
                cand = (idx + k) % n
                if jogadores[cand].estado == 'ativo':
                    return cand
            return None

        if len(vivos) == 2:
            idx_sb = idx_d if jogadores[idx_d].estado == 'ativo' else proximo_ativo(idx_d)
            idx_bb = proximo_ativo(idx_sb)
        else:
            idx_sb = proximo_ativo(idx_d)
            idx_bb = proximo_ativo(idx_sb)

        sb = self.__mesa.small_blind
        bb = self.__mesa.big_blind
        self.__mesa.receber_aposta(jogadores[idx_sb], sb)
        self.__mesa.receber_aposta(jogadores[idx_bb], bb)
        self.__mesa.aposta_atual = bb

    def distribuir_cartas_privadas(self):
        jogadores = self.__mesa.jogadores
        baralho = self.__mesa.baralho
        for _ in range(2):
            for j in jogadores:
                if j.fichas > 0 or j.estado == 'allin':
                    j.receber_carta(baralho.comprar())

    def avancar_estado(self):
        ordem = ['pre_flop', 'flop', 'turn', 'river', 'showdown', 'encerrada']
        if self.__estado not in ordem:
            raise ValueError(f"Não é possível avançar a partir de '{self.__estado}'.")
        idx = ordem.index(self.__estado)
        if idx + 1 >= len(ordem):
            return
        self.__estado = ordem[idx + 1]
        if self.__estado == 'flop':
            self.__mesa.colocar_comunitarias(3)
            _tela_publica("FLOP", [f"  Cartas: {' '.join(str(c) for c in self.__mesa.cartas_comunitarias)}", f"  Pote: {self.__mesa.pote.total}"])
        elif self.__estado == 'turn':
            self.__mesa.colocar_comunitarias(1)
            _tela_publica("TURN", [f"  Cartas: {' '.join(str(c) for c in self.__mesa.cartas_comunitarias)}", f"  Pote: {self.__mesa.pote.total}"])
        elif self.__estado == 'river':
            self.__mesa.colocar_comunitarias(1)
            _tela_publica("RIVER", [f"  Cartas: {' '.join(str(c) for c in self.__mesa.cartas_comunitarias)}", f"  Pote: {self.__mesa.pote.total}"])

    def executar_rodada_apostas(self):
        candidatos = [j for j in self.__mesa.jogadores if j.estado in ('ativo', 'allin')]
        if len(candidatos) <= 1:
            return False

        ativos = [j for j in self.__mesa.jogadores if j.estado == 'ativo']
        if len(ativos) <= 1:
            # Todos all-in ou só 1 ativo: não há mais apostas a fazer
            return True

        # Pós-flop: zera aposta_atual e aposta_rodada (pré-flop mantém os blinds)
        if self.__estado != 'pre_flop':
            self.__mesa.aposta_atual = 0
            for j in self.__mesa.jogadores:
                j.resetar_para_nova_rodada()

        jogadores = self.__mesa.jogadores
        n = len(jogadores)
        idx_d = self.__mesa.indice_dealer
        inicio = (idx_d + 3) % n if self.__estado == 'pre_flop' else (idx_d + 1) % n

        ja_agiu = {j.nome: False for j in jogadores}
        idx = inicio
        seguranca = 0
        max_passos = n * 20

        while seguranca < max_passos:
            seguranca += 1
            jogador = jogadores[idx]

            if jogador.estado == 'ativo':
                precisa_agir = (
                    not ja_agiu[jogador.nome]
                    or jogador.aposta_rodada < self.__mesa.aposta_atual
                )
                if precisa_agir:
                    aposta_antes = self.__mesa.aposta_atual
                    estado_pub = self.__mesa.estado_publico(jogador)
                    acao = jogador.decidir_acao(estado_pub)
                    if not isinstance(acao, Acao):
                        raise ValueError("decidir_acao deve retornar instância de Acao.")
                    acao.executar(jogador, self.__mesa)
                    ja_agiu[jogador.nome] = True
                    if self.__mesa.aposta_atual > aposta_antes:
                        # Aumento: todos os outros que já agiram precisam responder
                        for outro in jogadores:
                            if outro.nome != jogador.nome and outro.estado == 'ativo':
                                ja_agiu[outro.nome] = False

            candidatos = [j for j in jogadores if j.estado in ('ativo', 'allin')]
            if len(candidatos) <= 1:
                return False

            ativos = [j for j in jogadores if j.estado == 'ativo']
            if not ativos:
                break
            if all(ja_agiu[j.nome] and j.aposta_rodada == self.__mesa.aposta_atual for j in ativos):
                break

            idx = (idx + 1) % n

        return True

    def executar_showdown(self):
        candidatos = [j for j in self.__mesa.jogadores if j.estado in ('ativo', 'allin')]
        if not candidatos:
            return []
        if len(candidatos) == 1:
            return [candidatos[0].nome]

        comunit = self.__mesa.cartas_comunitarias
        avaliacoes = {}
        linhas = [f"  Comunitárias: {' '.join(str(c) for c in comunit)}", ""]
        for j in candidatos:
            cartas = j.mao + comunit
            resultado = AvaliadorMao.avaliar(cartas)
            avaliacoes[j.nome] = resultado
            descricao = AvaliadorMao.descrever(resultado[0], resultado[1])
            cartas_str = ' '.join(str(c) for c in j.mao)
            linhas.append(f"  {j.nome}: {cartas_str}  →  {descricao}")
        _tela_publica("SHOWDOWN", linhas)

        melhor = max(avaliacoes.values())
        vencedores = [nome for nome, res in avaliacoes.items() if res == melhor]
        return vencedores

    def encerrar_partida(self):
        candidatos = [j for j in self.__mesa.jogadores if j.estado in ('ativo', 'allin')]
        por_desistencia = False
        if len(candidatos) <= 1:
            vencedores = [candidatos[0].nome] if candidatos else []
            por_desistencia = True
        else:
            vencedores = self.executar_showdown()

        distribuicao = self.__mesa.pote.distribuir(vencedores)
        linhas = []
        if por_desistencia and vencedores:
            linhas.append(f"  Vencedor por desistência: {vencedores[0]}")
        elif len(vencedores) > 1:
            linhas.append(f"  Empate: {', '.join(vencedores)}")
        else:
            linhas.append(f"  Vencedor: {vencedores[0]}" if vencedores else "  Sem vencedor.")
        linhas.append("")
        for nome, valor in distribuicao.items():
            for j in self.__mesa.jogadores:
                if j.nome == nome:
                    j.receber_premio(valor)
                    linhas.append(f"  {nome} recebe {valor} fichas (total: {j.fichas})")
                    break
        linhas.append("")
        linhas.append("  Saldo atual:")
        for j in self.__mesa.jogadores:
            linhas.append(f"    {j.nome}: {j.fichas} fichas")
        _tela_publica("FIM DA MÃO", linhas)
        self.estado = 'encerrada'
        return {"vencedores": vencedores, "distribuicao": distribuicao}
