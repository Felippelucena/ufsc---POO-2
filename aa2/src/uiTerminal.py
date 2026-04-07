from src.app import App

class UiTerminal:
    def __init__(self):
        self.app = App()

    def iniciar(self):
        self.menu_inicial()

    def menu_inicial(self):
        print("")
        print("Bem-vindo ao Controle Financeiro Residencial!")
        print("1. Cadastrar Usuário | 2. Entrar | 0. Sair")

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            self.cadastrar_usuario()
            self.perfil()
        elif escolha == '2':
            if self.entrar_usuario():
                self.perfil()
        elif escolha == '0':
            print("Saindo...")
            return
        else:
            print("Opção inválida!")

        self.menu_inicial()

    def cadastrar_usuario(self):
        try:
            user = {
                "nome": input("Nome: "),
                "email": input("Email: "),
            }
            self.app.adicionar_usuario(user)

        except ValueError as e:
            print(f"Entrada inválida: {e}")
            self.cadastrar_usuario()

    def entrar_usuario(self):
        nome = input("Digite seu nome para entrar: ")
        if self.app.entrar_usuario(nome):
            return True
        else:
            print("Usuário não encontrado. Retornando ao menu inicial.")
            return False

    def perfil(self):
        print("")
        if not self.app.usuario_logado:
            return print("Usuário não logado. Retornando ao menu inicial.")

        u = self.app.usuario_logado
        cf = u.controle_financeiro
        print(f'----- Controle Financeiro Residencial -----')
        print(f"Bem-vindo, {u.nome} | Email: {u.email}")
        print(f"Total geral de despesas: R$ {cf.total_geral():.2f}")

        # Exibir alertas automaticamente
        alertas = self.app.verificar_alertas()
        if alertas:
            print("\n--- Alertas ---")
            for alerta in alertas:
                print(f"  {alerta}")
            print("---------------")

        print("")
        print("1. Registrar Despesa | 2. Ver Despesas por Categoria | 3. Relatório Mensal")
        print("4. Comparar Meses | 5. Definir Limites | 6. Exportar PDF")
        print("7. Atualizar Perfil | 0. Sair")

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            self.registrar_despesa()
        elif escolha == '2':
            self.ver_despesas()
        elif escolha == '3':
            self.relatorio_mensal()
        elif escolha == '4':
            self.comparar_meses()
        elif escolha == '5':
            self.definir_limites()
        elif escolha == '6':
            self.exportar_pdf()
        elif escolha == '7':
            self.atualizar_perfil()
        elif escolha == '0':
            print("Saindo...")
            self.app.logout()
            return
        else:
            print("Opção inválida!")

        self.perfil()

    def registrar_despesa(self):
        if not self.app.usuario_logado:
            return print("Usuário não logado.")

        categorias = list(self.app.usuario_logado.controle_financeiro.categorias.keys())
        print("\nCategorias disponíveis:")
        for i, cat in enumerate(categorias):
            print(f"  {i + 1}. {cat}")

        try:
            escolha = int(input("Escolha a categoria (número): ")) - 1
            if escolha < 0 or escolha >= len(categorias):
                return print("Categoria inválida.")

            categoria = categorias[escolha]
            valor = float(input("Valor (R$): "))
            data = input("Data (DD/MM/AAAA): ")
            descricao = input("Descrição: ")

            self.app.adicionar_despesa({
                "valor": valor,
                "categoria": categoria,
                "data": data,
                "descricao": descricao
            })
            print(f"Despesa de R$ {valor:.2f} registrada em {categoria}.")

            # Verificar alerta da categoria após adicionar
            cf = self.app.usuario_logado.controle_financeiro
            alerta = cf.categorias[categoria].alerta
            if alerta:
                print(f"\n  {alerta}")

        except ValueError as e:
            print(f"Entrada inválida: {e}")

    def ver_despesas(self):
        if not self.app.usuario_logado:
            return print("Usuário não logado.")

        cf = self.app.usuario_logado.controle_financeiro
        print("\n----- Despesas por Categoria -----")
        for nome, cat in cf.categorias.items():
            despesas = cat.despesas
            limite_str = f"R$ {cat.limite:.2f}" if cat.limite else "Sem limite"
            print(f"\n{nome} (Limite: {limite_str}) — Total: R$ {cat.total:.2f}")
            if despesas:
                for i, d in enumerate(despesas):
                    print(f"  {i + 1}. {d}")
            else:
                print("  Nenhuma despesa registrada.")

    def relatorio_mensal(self):
        if not self.app.usuario_logado:
            return print("Usuário não logado.")

        mes_ano = input("Digite o mês/ano (MM/AAAA): ")
        relatorio = self.app.relatorio_mensal(mes_ano)
        total_geral = relatorio.pop("TOTAL", 0)

        print(f"\n========== Relatório Mensal — {mes_ano} ==========")
        for nome, dados in relatorio.items():
            total = dados['total']
            limite = dados['limite']
            limite_str = f"R$ {limite:.2f}" if limite else "---"
            status = ""
            if limite and total >= limite:
                status = " ACIMA DO LIMITE"
            elif limite and total >= limite * 0.8:
                status = " ATENCAO"

            print(f"  {nome:<20} R$ {total:>10.2f} / {limite_str}{status}")

        print(f"  {'':─<55}")
        print(f"  {'TOTAL':<20} R$ {total_geral:>10.2f}")
        print(f"{'='*50}")

    def comparar_meses(self):
        if not self.app.usuario_logado:
            return print("Usuário não logado.")

        mes1 = input("Primeiro mês (MM/AAAA): ")
        mes2 = input("Segundo mês (MM/AAAA): ")
        comparacao = self.app.comparar_meses(mes1, mes2)

        print(f"\n========== Comparação: {mes1} vs {mes2} ==========")
        print(f"  {'Categoria':<20} {mes1:>10} {mes2:>10} {'Diferença':>10} {'%':>8}")
        print(f"  {'':─<60}")

        for nome, dados in comparacao.items():
            sinal = "+" if dados['diferenca'] >= 0 else ""
            alerta = " !!" if dados['aumento_significativo'] else ""
            print(f"  {nome:<20} R$ {dados['mes1']:>7.2f} R$ {dados['mes2']:>7.2f} {sinal}{dados['diferenca']:>8.2f} {dados['percentual']:>7.1f}%{alerta}")

        print(f"{'='*60}")

    def definir_limites(self):
        if not self.app.usuario_logado:
            return print("Usuário não logado.")

        cf = self.app.usuario_logado.controle_financeiro
        print("\nLimites atuais:")
        categorias = list(cf.categorias.keys())
        for i, nome in enumerate(categorias):
            cat = cf.categorias[nome]
            limite_str = f"R$ {cat.limite:.2f}" if cat.limite else "Sem limite"
            print(f"  {i + 1}. {nome}: {limite_str}")

        try:
            escolha = int(input("Escolha a categoria para alterar o limite (número): ")) - 1
            if escolha < 0 or escolha >= len(categorias):
                return print("Categoria inválida.")

            categoria = categorias[escolha]
            novo_limite = float(input(f"Novo limite para {categoria} (R$): "))
            self.app.definir_limite(categoria, novo_limite)
            print(f"Limite de {categoria} atualizado para R$ {novo_limite:.2f}.")

        except ValueError as e:
            print(f"Entrada inválida: {e}")

    def exportar_pdf(self):
        if not self.app.usuario_logado:
            return print("Usuário não logado.")

        mes_ano = input("Mês/ano para o relatório PDF (MM/AAAA): ")
        try:
            caminho = self.app.exportar_pdf(mes_ano)
            print(f"Relatório exportado com sucesso: {caminho}")
        except ImportError:
            print("Biblioteca fpdf não encontrada. Instale com: pip install fpdf2")
        except Exception as e:
            print(f"Erro ao exportar PDF: {e}")

    def atualizar_perfil(self):
        if not self.app.usuario_logado:
            return print("Usuário não logado.")

        u = self.app.usuario_logado
        print("\nAtualizar Perfil (pressione Enter para manter o valor atual):")

        try:
            dados = {}

            email = input(f"Email ({u.email}): ").strip()
            if email:
                dados['email'] = email

            if dados:
                self.app.atualizar_usuario(dados)
                print("Perfil atualizado com sucesso!")
            else:
                print("Nenhuma alteração realizada.")

        except ValueError as e:
            print(f"Entrada inválida: {e}")
