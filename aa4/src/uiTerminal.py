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
        nome = input("Seu nome: ").strip()
        if len(nome) < 2:
            print("Nome muito curto. Voltando ao menu.")
            return
        while True:
            entrada = input("Número de oponentes IA (1 a 3) [2]: ").strip() or '2'
            if entrada.isdigit() and 1 <= int(entrada) <= 3:
                n_ias = int(entrada)
                break
            print("Valor inválido.")
        while True:
            entrada = input("Fichas iniciais por jogador [1000]: ").strip() or '1000'
            if entrada.isdigit() and int(entrada) >= 100:
                fichas = int(entrada)
                break
            print("Valor inválido (mínimo 100).")

        try:
            self.__app.configurar_partida(nome_humano=nome, n_ias=n_ias, fichas_iniciais=fichas)
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
