from src.app import App

'''
Classe UiTerminal
Interface CLI recursiva: menu inicial → configurar partida → jogar → voltar.
'''


class UiTerminal:
    def __init__(self):
        self.__app = App()

    def iniciar(self):
        print("\n========================================")
        print("       POKER TEXAS HOLD'EM — aa4         ")
        print("========================================")
        self.menu_inicial()

    def menu_inicial(self):
        print("")
        print("=== Menu ===")
        print("1. Iniciar Nova Partida")
        print("2. Ver Ranking")
        print("0. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == '1':
            self.configurar_partida()
        elif escolha == '2':
            self.exibir_ranking()
        elif escolha == '0':
            print("Até a próxima!")
            return
        else:
            print("Opção inválida!")
        self.menu_inicial()

    def configurar_partida(self):
        while True:
            entrada = input("Quantos jogadores? (2 a 4): ").strip()
            if entrada.isdigit() and 2 <= int(entrada) <= 4:
                n_jogadores = int(entrada)
                break
            print("Valor inválido.")

        nomes = []
        for i in range(1, n_jogadores + 1):
            while True:
                nome = input(f"Nome do jogador {i}: ").strip()
                if len(nome) < 2:
                    print("Nome muito curto.")
                    continue
                if nome in nomes:
                    print("Nome já usado.")
                    continue
                nomes.append(nome)
                break

        while True:
            entrada = input("Fichas iniciais por jogador [1000]: ").strip() or '1000'
            if entrada.isdigit() and int(entrada) >= 100:
                fichas = int(entrada)
                break
            print("Valor inválido (mínimo 100).")

        try:
            self.__app.configurar_partida(nomes=nomes, fichas_iniciais=fichas)
        except ValueError as e:
            print(f"Erro ao configurar: {e}")
            return

        resumo = self.__app.jogar_partida()
        print("\n========================================")
        print(f"   FIM DA SESSÃO — Vencedor: {resumo['vencedor']}")
        print(f"   Fichas finais: {resumo['fichas_finais']}")
        print("========================================")

    def exibir_ranking(self):
        ranking = self.__app.listar_ranking(top=10)
        print("\n=== TOP 10 RANKING ===")
        if not ranking:
            print("(ainda não há partidas registradas)")
            return
        for i, r in enumerate(ranking, start=1):
            print(f"  {i:>2}. {r.get('vencedor','?'):<20} {r.get('fichas_finais',0):>6} fichas  ({r.get('n_jogadores','?')} jog.)  {r.get('data','')}")
