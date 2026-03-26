from src.app import App

class UiTerminal:
    def __init__(self):
        self.app = App()

    def iniciar(self):
        self.menu_inicial()
    
    def menu_inicial(self):
        print("")
        print("Bem-vindo ao Dieta em Dia!")
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
                "sexo": input("Sexo (m/f): "),
                "idade": int(input("Idade: ")),
                "peso": float(input("Peso (kg): ")),
                "altura": float(input("Altura (cm): ")),
                "objetivo": input("Objetivo (perda de peso, manutenção, ganho de massa): "),
                "nivel_atividade": input("Nível de Atividade (sedentario, leve, moderado, intenso, muito intenso): ")
            }
            self.app.adicionar_usuario(user)
            
        except ValueError as e:
            print(f"Entrada inválida: {e}")
            self.cadastrar_usuario()
            
    def perfil(self):
        print("")
        if not self.app.usuario_logado: return print("Usuário não logado. Retornando ao menu inicial.")
        
        print(f'----- Dashboard Dieta em Dia -----')
        print(f"Bem-vindo, {self.app.usuario_logado.nome} | Idade: {self.app.usuario_logado.idade}, Peso: {self.app.usuario_logado.peso}kg, Altura: {self.app.usuario_logado.altura}cm")
        print(f'Objetivo: {self.app.usuario_logado.objetivo} | Nível de Atividade: {self.app.usuario_logado.nivel_atividade} | TMB: {self.app.usuario_logado.tmb:.2f} kcal | GET: {self.app.usuario_logado.get:.2f} kcal')
        print('1. Registrar Consumo do Dia | 2. Ver Alimentos Cadastrados | 3. Cadastrar Novo Alimento')
        print('4. Atualizar Perfil | 5. Ver Histórico de Consumo | 6. Gerar Relatório | 0. Sair')
        
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            self.registrar_consumo_do_dia()
        elif escolha == '2':
            self.alimentos_disponiveis()
        elif escolha == '3':
            self.cadastrar_alimento()
        elif escolha == '4':
            self.atualizar_perfil()
        elif escolha == '5':
            self.historico_consumo()
        elif escolha == '6':
            self.gerar_relatorio()
        elif escolha == '0':
            print("Saindo...")
            self.app.logout()
            return
        else:
            print("Opção inválida!")
        
        self.perfil()
        
    def alimentos_disponiveis(self):
        print("")
        print("Alimentos Globais:")
        for alimento in self.app.alimentos:
            print(f"{alimento.nome} - {alimento.porcao}g - {alimento.calorias:.2f} kcal")
        print("Seus Alimentos:")
        for i, alimento in enumerate(self.app.usuario_logado.alimentos):
            print(f"{i + 1}. {alimento.nome} - {alimento.porcao}g - {alimento.calorias:.2f} kcal")
            

    def entrar_usuario(self):
        nome = input("Digite seu nome para entrar: ")
        if self.app.entrar_usuario(nome):
            return True
        else:
            print("Usuário não encontrado. Retornando ao menu inicial.")
            return False
        
    
    def registrar_consumo_do_dia(self):
        if not self.app.usuario_logado: return print("Usuário não logado. Retornando ao menu inicial.")
        print("Alimentos disponíveis:")
        todos_alimentos = self.app.alimentos + self.app.usuario_logado.alimentos
        consumo_do_dia = []
        
        for i, alimento in enumerate(todos_alimentos):
            print(f"{i + 1}. {alimento.nome} - {alimento.porcao}g - {alimento.calorias:.2f} kcal")
        
        data = input("Digite a data do consumo (YYYY-MM-DD): ")
        
        #verificar se a data é valida
        try:
            from datetime import datetime
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            print("Data inválida. Por favor, digite no formato YYYY-MM-DD.")
            return

        escolha = input("Digite o número do alimento consumido (ou 0 para finalizar): ")
        while escolha != '0':
            try:
                index = int(escolha) - 1
                if 0 <= index < len(todos_alimentos):
                    alimento = todos_alimentos[index]
                    quantia = float(input(f"Quantia consumida de {alimento.nome} (g): "))
                    consumo_do_dia.append([alimento.nome, quantia, alimento.calorias_consumidas(quantia)])
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
            
            escolha = input("Digite o número do alimento consumido (ou 0 para finalizar): ")
        
        self.app.registrar_consumo_diario(data, consumo_do_dia)

        # Resumo diário com comparação à meta
        total = sum(item[2] for item in consumo_do_dia)
        meta = self.app.usuario_logado.get
        diff = total - meta

        print(f"\n----- Resumo do dia {data} -----")
        for item in consumo_do_dia:
            print(f"  {item[0]} — {item[1]}g — {item[2]:.2f} kcal")
        print(f"Total consumido: {total:.2f} kcal | Meta (GET): {meta:.2f} kcal")
        if diff > 0:
            print(f"Acima da meta em {diff:.2f} kcal.")
        elif diff < 0:
            print(f"Abaixo da meta em {abs(diff):.2f} kcal.")
        else:
            print("Exatamente na meta!")
    
    def gerar_relatorio(self):
        if not self.app.usuario_logado: return print("Usuário não logado.")

        consumo = self.app.usuario_logado.consumo_diario
        if not consumo:
            return print("\nNenhum consumo registrado para gerar relatório.")

        u = self.app.usuario_logado
        meta = u.get
        dias = sorted(consumo.keys())
        totais = [sum(item[2] for item in consumo[d]) for d in dias]

        media = sum(totais) / len(totais)
        melhor_dia = dias[totais.index(min(totais, key=lambda t: abs(t - meta)))]
        dias_acima = sum(1 for t in totais if t > meta)
        dias_abaixo = sum(1 for t in totais if t < meta)

        print(f"\n========== Relatório Nutricional ==========")
        print(f"Usuário: {u.nome} | Objetivo: {u.objetivo}")
        print(f"TMB: {u.tmb:.2f} kcal | GET (meta): {meta:.2f} kcal")
        print(f"Período: {dias[0]} a {dias[-1]} ({len(dias)} dias registrados)")
        print(f"-------------------------------------------")
        print(f"Média diária consumida: {media:.2f} kcal")
        print(f"Dia mais próximo da meta: {melhor_dia}")
        print(f"Dias acima da meta: {dias_acima} | Dias abaixo da meta: {dias_abaixo}")
        print(f"-------------------------------------------")

        for i, data in enumerate(dias):
            diff = totais[i] - meta
            status = "+" if diff >= 0 else ""
            print(f"  {data}:  {totais[i]:>8.2f} kcal  ({status}{diff:.2f})")

        print(f"===========================================")

    def historico_consumo(self):
        if not self.app.usuario_logado: return print("Usuário não logado.")

        consumo = self.app.usuario_logado.consumo_diario
        if not consumo:
            return print("\nNenhum consumo registrado.")

        meta = self.app.usuario_logado.get
        print(f"\n----- Histórico de Consumo (Meta diária: {meta:.2f} kcal) -----")

        for data in sorted(consumo.keys()):
            itens = consumo[data]
            total = sum(item[2] for item in itens)
            diff = total - meta

            print(f"\n📅 {data} — Total: {total:.2f} kcal", end="")
            if diff > 0:
                print(f"  (acima da meta em {diff:.2f} kcal)")
            elif diff < 0:
                print(f"  (abaixo da meta em {abs(diff):.2f} kcal)")
            else:
                print(f"  (na meta!)")

            for item in itens:
                print(f"   {item[0]} — {item[1]}g — {item[2]:.2f} kcal")

    def atualizar_perfil(self):
        if not self.app.usuario_logado: return print("Usuário não logado.")

        u = self.app.usuario_logado
        print("\nAtualizar Perfil (pressione Enter para manter o valor atual):")

        try:
            dados = {}

            sexo = input(f"Sexo ({u.sexo}): ").strip()
            if sexo: dados['sexo'] = sexo

            idade = input(f"Idade ({u.idade}): ").strip()
            if idade: dados['idade'] = int(idade)

            peso = input(f"Peso ({u.peso}kg): ").strip()
            if peso: dados['peso'] = float(peso)

            altura = input(f"Altura ({u.altura}cm): ").strip()
            if altura: dados['altura'] = float(altura)

            objetivo = input(f"Objetivo ({u.objetivo}) [perda de peso / manutenção / ganho de massa]: ").strip()
            if objetivo: dados['objetivo'] = objetivo

            nivel = input(f"Nível de Atividade ({u.nivel_atividade}) [sedentario / leve / moderado / intenso / muito intenso]: ").strip()
            if nivel: dados['nivel_atividade'] = nivel

            if dados:
                self.app.atualizar_usuario(dados)
                print("Perfil atualizado com sucesso!")
            else:
                print("Nenhuma alteração realizada.")

        except ValueError as e:
            print(f"Entrada inválida: {e}")

    def cadastrar_alimento(self):
        try:
            alimento = {
                "nome": input("Nome do alimento: "),
                "porcao": float(input("Porção (g): ")),
                "proteina": float(input("Proteína (g): ")),
                "carboidrato": float(input("Carboidrato (g): ")),
                "gordura": float(input("Gordura (g): ")),
            }
            self.app.alterar_alimentos_usuario(alimento, "adicionar")
            
        except ValueError as e:
            print(f"Entrada inválida: {e}")
            self.cadastrar_alimento()
