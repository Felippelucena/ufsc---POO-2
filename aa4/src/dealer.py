from src.mesa import Mesa
from src.avaliadorMao import AvaliadorMao

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
        print(f"\n=== Nova mão começou — dealer: {self.__mesa.jogadores[self.__mesa.indice_dealer].nome} ===")

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
        print(f"  Blinds: {jogadores[idx_sb].nome} (SB {sb}) | {jogadores[idx_bb].nome} (BB {bb})")

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
            print(f"\n  -- FLOP: {' '.join(str(c) for c in self.__mesa.cartas_comunitarias)}")
        elif self.__estado == 'turn':
            self.__mesa.colocar_comunitarias(1)
            print(f"\n  -- TURN: {' '.join(str(c) for c in self.__mesa.cartas_comunitarias)}")
        elif self.__estado == 'river':
            self.__mesa.colocar_comunitarias(1)
            print(f"\n  -- RIVER: {' '.join(str(c) for c in self.__mesa.cartas_comunitarias)}")

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
                    decisao = jogador.decidir_acao(estado_pub)
                    self._processar_decisao(jogador, decisao)
                    ja_agiu[jogador.nome] = True
                    print(f"  {jogador.nome}: {decisao['acao']}" + (f" {decisao['valor']}" if decisao.get('valor') else ""))
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

    def _processar_decisao(self, jogador, decisao):
        acao = decisao.get('acao')
        valor = decisao.get('valor', 0)
        if acao == 'passar':
            return
        if acao == 'desistir':
            jogador.desistir()
            return
        if acao == 'pagar':
            diff = self.__mesa.aposta_atual - jogador.aposta_rodada
            self.__mesa.receber_aposta(jogador, diff)
            return
        if acao == 'aumentar':
            self.__mesa.receber_aposta(jogador, valor)
            return
        if acao == 'all_in':
            self.__mesa.receber_aposta(jogador, jogador.fichas)
            return
        raise ValueError(f"Ação desconhecida: {acao}")

    def executar_showdown(self):
        candidatos = [j for j in self.__mesa.jogadores if j.estado in ('ativo', 'allin')]
        if not candidatos:
            return []
        if len(candidatos) == 1:
            return [candidatos[0].nome]

        comunit = self.__mesa.cartas_comunitarias
        avaliacoes = {}
        print("\n  -- SHOWDOWN --")
        for j in candidatos:
            cartas = j.mao + comunit
            resultado = AvaliadorMao.avaliar(cartas)
            avaliacoes[j.nome] = resultado
            descricao = AvaliadorMao.descrever(resultado[0], resultado[1])
            cartas_str = ' '.join(str(c) for c in j.mao)
            print(f"  {j.nome}: {cartas_str}  →  {descricao}")

        melhor = max(avaliacoes.values())
        vencedores = [nome for nome, res in avaliacoes.items() if res == melhor]
        return vencedores

    def encerrar_partida(self):
        candidatos = [j for j in self.__mesa.jogadores if j.estado in ('ativo', 'allin')]
        if len(candidatos) <= 1:
            vencedores = [candidatos[0].nome] if candidatos else []
            if vencedores:
                print(f"\n  Vencedor por desistência: {vencedores[0]}")
        else:
            vencedores = self.executar_showdown()

        distribuicao = self.__mesa.pote.distribuir(vencedores)
        for nome, valor in distribuicao.items():
            for j in self.__mesa.jogadores:
                if j.nome == nome:
                    j.receber_premio(valor)
                    print(f"  {nome} recebe {valor} fichas (total: {j.fichas})")
                    break
        self.estado = 'encerrada'
        return {"vencedores": vencedores, "distribuicao": distribuicao}
