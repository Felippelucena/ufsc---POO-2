import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from src.app import App


class Ui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dieta em Dia")
        self.geometry("800x600")
        self.minsize(700, 500)

        self.app = App()

        # Container principal que empilha todas as páginas
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._criar_paginas_iniciais()
        self.show_frame("MenuPage")

    def _criar_paginas_iniciais(self):
        for Page in (MenuPage, LoginPage, CadastroPage):
            self._registrar_pagina(Page)

    def _registrar_pagina(self, Page):
        page_name = Page.__name__
        frame = Page(parent=self.container, controller=self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "ao_exibir"):
            frame.ao_exibir()
        frame.tkraise()

    def ir_para_dashboard(self):
        if "DashboardPage" not in self.frames:
            self._registrar_pagina(DashboardPage)
            self._registrar_pagina(RegistrarConsumoPage)
            self._registrar_pagina(AlimentosPage)
            self._registrar_pagina(CadastrarAlimentoPage)
            self._registrar_pagina(AtualizarPerfilPage)
            self._registrar_pagina(HistoricoPage)
            self._registrar_pagina(RelatorioPage)
        self.show_frame("DashboardPage")

    def logout(self):
        self.app.logout()
        # Remove páginas do dashboard para recriar com dados novos no próximo login
        for page in ("DashboardPage", "RegistrarConsumoPage", "AlimentosPage",
                      "CadastrarAlimentoPage", "AtualizarPerfilPage", "HistoricoPage", "RelatorioPage"):
            if page in self.frames:
                self.frames[page].destroy()
                del self.frames[page]
        self.show_frame("MenuPage")


# ===================== MENU INICIAL =====================

class MenuPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        ttk.Label(self, text="Dieta em Dia", font=("Helvetica", 22, "bold")).pack(pady=(30, 5))
        ttk.Label(self, text="Sistema de Controle de Dieta e Nutrição", font=("Helvetica", 11)).pack(pady=(0, 30))

        ttk.Button(self, text="Entrar", width=25, command=lambda: controller.show_frame("LoginPage")).pack(pady=5)
        ttk.Button(self, text="Cadastrar Usuário", width=25, command=lambda: controller.show_frame("CadastroPage")).pack(pady=5)
        ttk.Button(self, text="Sair", width=25, command=controller.destroy).pack(pady=20)


# ===================== LOGIN =====================

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        ttk.Label(self, text="Login", font=("Helvetica", 18, "bold")).pack(pady=(30, 20))

        ttk.Label(self, text="Nome:").pack(anchor="w", padx=100)
        self.nome_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nome_var, width=40).pack(pady=(0, 15))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Entrar", command=self._entrar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("MenuPage")).grid(row=0, column=1, padx=5)

    def _entrar(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite seu nome.")
            return
        if self.controller.app.entrar_usuario(nome):
            self.nome_var.set("")
            self.controller.ir_para_dashboard()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")


# ===================== CADASTRO =====================

class CadastroPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="Cadastrar Usuário", font=("Helvetica", 18, "bold")).pack(pady=(10, 15))

        form = ttk.Frame(self)
        form.pack()

        self.campos = {}
        labels = [("Nome", "nome"), ("Sexo (m/f)", "sexo"), ("Idade", "idade"),
                  ("Peso (kg)", "peso"), ("Altura (cm)", "altura")]

        for i, (label, key) in enumerate(labels):
            ttk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="w", pady=3, padx=(0, 10))
            var = tk.StringVar()
            ttk.Entry(form, textvariable=var, width=30).grid(row=i, column=1, pady=3)
            self.campos[key] = var

        row_offset = len(labels)

        ttk.Label(form, text="Objetivo:").grid(row=row_offset, column=0, sticky="w", pady=3, padx=(0, 10))
        self.objetivo_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.objetivo_var, width=28, state="readonly",
                     values=["perda de peso", "manutenção", "ganho de massa"]).grid(row=row_offset, column=1, pady=3)

        ttk.Label(form, text="Nível de Atividade:").grid(row=row_offset + 1, column=0, sticky="w", pady=3, padx=(0, 10))
        self.nivel_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.nivel_var, width=28, state="readonly",
                     values=["sedentario", "leve", "moderado", "intenso", "muito intenso"]).grid(row=row_offset + 1, column=1, pady=3)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Cadastrar", command=self._cadastrar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("MenuPage")).grid(row=0, column=1, padx=5)

    def _cadastrar(self):
        try:
            user = {
                "nome": self.campos["nome"].get().strip(),
                "sexo": self.campos["sexo"].get().strip(),
                "idade": int(self.campos["idade"].get()),
                "peso": float(self.campos["peso"].get()),
                "altura": float(self.campos["altura"].get()),
                "objetivo": self.objetivo_var.get(),
                "nivel_atividade": self.nivel_var.get(),
            }
            self.controller.app.adicionar_usuario(user)
            # Limpar campos
            for var in self.campos.values():
                var.set("")
            self.objetivo_var.set("")
            self.nivel_var.set("")
            messagebox.showinfo("Sucesso", f"Usuário {user['nome']} cadastrado!")
            self.controller.ir_para_dashboard()
        except (ValueError, KeyError) as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")


# ===================== DASHBOARD =====================

class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        self.header = ttk.Label(self, text="", font=("Helvetica", 16, "bold"))
        self.header.pack(pady=(10, 5))

        self.info_label = ttk.Label(self, text="", font=("Helvetica", 10))
        self.info_label.pack(pady=(0, 5))

        self.stats_label = ttk.Label(self, text="", font=("Helvetica", 10))
        self.stats_label.pack(pady=(0, 15))

        sep = ttk.Separator(self, orient="horizontal")
        sep.pack(fill="x", padx=20, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        botoes = [
            ("Registrar Consumo do Dia", "RegistrarConsumoPage"),
            ("Ver Alimentos", "AlimentosPage"),
            ("Cadastrar Alimento", "CadastrarAlimentoPage"),
            ("Atualizar Perfil", "AtualizarPerfilPage"),
            ("Histórico de Consumo", "HistoricoPage"),
            ("Gerar Relatório", "RelatorioPage"),
        ]

        for i, (texto, pagina) in enumerate(botoes):
            r, c = divmod(i, 2)
            ttk.Button(btn_frame, text=texto, width=28,
                       command=lambda p=pagina: controller.show_frame(p)).grid(row=r, column=c, padx=5, pady=4)

        ttk.Button(self, text="Sair (Logout)", command=controller.logout).pack(pady=15)

    def ao_exibir(self):
        u = self.controller.app.usuario_logado
        if not u:
            return
        self.header.config(text=f"Bem-vindo, {u.nome}!")
        self.info_label.config(text=f"Idade: {u.idade} | Peso: {u.peso}kg | Altura: {u.altura}cm | Sexo: {u.sexo}")
        self.stats_label.config(
            text=f"Objetivo: {u.objetivo} | Atividade: {u.nivel_atividade} | TMB: {u.tmb:.2f} kcal | GET: {u.get:.2f} kcal"
        )


# ===================== REGISTRAR CONSUMO =====================

class RegistrarConsumoPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller
        self.consumo_do_dia = []

        ttk.Label(self, text="Registrar Consumo do Dia", font=("Helvetica", 16, "bold")).pack(pady=(5, 10))

        # Data
        data_frame = ttk.Frame(self)
        data_frame.pack(pady=5)
        ttk.Label(data_frame, text="Data (YYYY-MM-DD):").pack(side="left", padx=(0, 5))
        self.data_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(data_frame, textvariable=self.data_var, width=15).pack(side="left")

        # Lista de alimentos disponíveis
        ttk.Label(self, text="Alimentos disponíveis:").pack(anchor="w", padx=20, pady=(10, 0))
        self.lista_alimentos = tk.Listbox(self, height=8, width=60)
        self.lista_alimentos.pack(padx=20, pady=5)

        # Quantia
        q_frame = ttk.Frame(self)
        q_frame.pack(pady=5)
        ttk.Label(q_frame, text="Quantia (g):").pack(side="left", padx=(0, 5))
        self.quantia_var = tk.StringVar()
        ttk.Entry(q_frame, textvariable=self.quantia_var, width=10).pack(side="left", padx=(0, 10))
        ttk.Button(q_frame, text="Adicionar", command=self._adicionar_item).pack(side="left")

        # Consumo do dia
        ttk.Label(self, text="Consumo do dia:").pack(anchor="w", padx=20, pady=(10, 0))
        self.lista_consumo = tk.Listbox(self, height=6, width=60)
        self.lista_consumo.pack(padx=20, pady=5)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar Consumo", command=self._salvar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("DashboardPage")).grid(row=0, column=2, padx=5)

        # Resumo
        self.resumo_label = ttk.Label(self, text="", font=("Helvetica", 10))
        self.resumo_label.pack(pady=5)

    def ao_exibir(self):
        self._limpar()
        self.lista_alimentos.delete(0, "end")
        todos = self._todos_alimentos()
        for i, a in enumerate(todos):
            self.lista_alimentos.insert("end", f"{i+1}. {a.nome} — {a.porcao}g — {a.calorias} kcal")

    def _todos_alimentos(self):
        return self.controller.app.alimentos + self.controller.app.usuario_logado.alimentos

    def _adicionar_item(self):
        sel = self.lista_alimentos.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um alimento da lista.")
            return
        try:
            quantia = float(self.quantia_var.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Digite uma quantia válida em gramas.")
            return

        todos = self._todos_alimentos()
        alimento = todos[sel[0]]
        calorias = alimento.calorias_consumidas(quantia)
        self.consumo_do_dia.append([alimento.nome, quantia, calorias])
        self.lista_consumo.insert("end", f"{alimento.nome} — {quantia}g — {calorias:.2f} kcal")
        self.quantia_var.set("")

    def _salvar(self):
        if not self.consumo_do_dia:
            messagebox.showwarning("Aviso", "Adicione ao menos um alimento.")
            return
        data = self.data_var.get().strip()
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato YYYY-MM-DD.")
            return

        consumo_copia = [item[:] for item in self.consumo_do_dia]
        self.controller.app.registrar_consumo_diario(data, consumo_copia)

        # Resumo
        total = sum(item[2] for item in self.consumo_do_dia)
        meta = self.controller.app.usuario_logado.get
        diff = total - meta
        if diff > 0:
            status = f"Acima da meta em {diff:.2f} kcal"
        elif diff < 0:
            status = f"Abaixo da meta em {abs(diff):.2f} kcal"
        else:
            status = "Exatamente na meta!"

        self.resumo_label.config(text=f"Total: {total:.2f} kcal | Meta: {meta:.2f} kcal — {status}")
        messagebox.showinfo("Sucesso", f"Consumo de {data} registrado!\n{status}")

    def _limpar(self):
        self.consumo_do_dia.clear()
        self.lista_consumo.delete(0, "end")
        self.resumo_label.config(text="")
        self.quantia_var.set("")


# ===================== VER ALIMENTOS =====================

class AlimentosPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="Alimentos Cadastrados", font=("Helvetica", 16, "bold")).pack(pady=(5, 10))

        ttk.Label(self, text="Alimentos Globais:", font=("Helvetica", 11, "bold")).pack(anchor="w", padx=20)
        self.lista_global = tk.Listbox(self, height=7, width=70)
        self.lista_global.pack(padx=20, pady=5)

        ttk.Label(self, text="Seus Alimentos (selecione para editar/excluir):", font=("Helvetica", 11, "bold")).pack(anchor="w", padx=20)
        self.lista_usuario = tk.Listbox(self, height=6, width=70)
        self.lista_usuario.pack(padx=20, pady=5)

        # Formulário de edição
        self.edit_frame = ttk.LabelFrame(self, text="Editar Alimento Selecionado", padding=10)
        self.edit_frame.pack(padx=20, pady=5, fill="x")

        campos_frame = ttk.Frame(self.edit_frame)
        campos_frame.pack()

        self.edit_campos = {}
        labels = [("Porção (g)", "porcao"), ("Proteína (g)", "proteina"),
                  ("Carboidrato (g)", "carboidrato"), ("Gordura (g)", "gordura")]

        for i, (label, key) in enumerate(labels):
            ttk.Label(campos_frame, text=f"{label}:").grid(row=0, column=i * 2, padx=(5, 2), pady=3)
            var = tk.StringVar()
            ttk.Entry(campos_frame, textvariable=var, width=8).grid(row=0, column=i * 2 + 1, padx=(0, 5), pady=3)
            self.edit_campos[key] = var

        edit_btn_frame = ttk.Frame(self.edit_frame)
        edit_btn_frame.pack(pady=5)
        ttk.Button(edit_btn_frame, text="Atualizar", command=self._atualizar).grid(row=0, column=0, padx=5)
        ttk.Button(edit_btn_frame, text="Excluir", command=self._excluir).grid(row=0, column=1, padx=5)

        self.lista_usuario.bind("<<ListboxSelect>>", self._ao_selecionar)

        ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("DashboardPage")).pack(pady=10)

    def ao_exibir(self):
        self._atualizar_listas()
        self._limpar_edicao()

    def _atualizar_listas(self):
        self.lista_global.delete(0, "end")
        for a in self.controller.app.alimentos:
            self.lista_global.insert("end", f"{a.nome} — {a.porcao}g — {a.calorias} kcal | P:{a.proteina}g C:{a.carboidrato}g G:{a.gordura}g")

        self.lista_usuario.delete(0, "end")
        for a in self.controller.app.usuario_logado.alimentos:
            self.lista_usuario.insert("end", f"{a.nome} — {a.porcao}g — {a.calorias} kcal | P:{a.proteina}g C:{a.carboidrato}g G:{a.gordura}g")

    def _ao_selecionar(self, event):
        sel = self.lista_usuario.curselection()
        if not sel:
            return
        alimento = self.controller.app.usuario_logado.alimentos[sel[0]]
        self.edit_campos["porcao"].set(str(alimento.porcao))
        self.edit_campos["proteina"].set(str(alimento.proteina))
        self.edit_campos["carboidrato"].set(str(alimento.carboidrato))
        self.edit_campos["gordura"].set(str(alimento.gordura))

    def _get_selecionado(self):
        sel = self.lista_usuario.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um alimento seu da lista.")
            return None
        return self.controller.app.usuario_logado.alimentos[sel[0]]

    def _atualizar(self):
        alimento = self._get_selecionado()
        if not alimento:
            return
        try:
            dados = {
                "nome": alimento.nome,
                "porcao": float(self.edit_campos["porcao"].get()),
                "proteina": float(self.edit_campos["proteina"].get()),
                "carboidrato": float(self.edit_campos["carboidrato"].get()),
                "gordura": float(self.edit_campos["gordura"].get()),
            }
            self.controller.app.alterar_alimentos_usuario(dados, "atualizar")
            self._atualizar_listas()
            self._limpar_edicao()
            messagebox.showinfo("Sucesso", f"Alimento '{alimento.nome}' atualizado!")
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    def _excluir(self):
        alimento = self._get_selecionado()
        if not alimento:
            return
        if messagebox.askyesno("Confirmar", f"Excluir '{alimento.nome}'?"):
            self.controller.app.alterar_alimentos_usuario({"nome": alimento.nome}, "remover")
            self._atualizar_listas()
            self._limpar_edicao()
            messagebox.showinfo("Sucesso", f"Alimento '{alimento.nome}' excluído!")

    def _limpar_edicao(self):
        for var in self.edit_campos.values():
            var.set("")


# ===================== CADASTRAR ALIMENTO =====================

class CadastrarAlimentoPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="Cadastrar Novo Alimento", font=("Helvetica", 16, "bold")).pack(pady=(10, 15))

        form = ttk.Frame(self)
        form.pack()

        self.campos = {}
        labels = [("Nome", "nome"), ("Porção (g)", "porcao"),
                  ("Proteína (g)", "proteina"), ("Carboidrato (g)", "carboidrato"), ("Gordura (g)", "gordura")]

        for i, (label, key) in enumerate(labels):
            ttk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="w", pady=3, padx=(0, 10))
            var = tk.StringVar()
            ttk.Entry(form, textvariable=var, width=25).grid(row=i, column=1, pady=3)
            self.campos[key] = var

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Cadastrar", command=self._cadastrar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("DashboardPage")).grid(row=0, column=1, padx=5)

    def _cadastrar(self):
        try:
            alimento = {
                "nome": self.campos["nome"].get().strip(),
                "porcao": float(self.campos["porcao"].get()),
                "proteina": float(self.campos["proteina"].get()),
                "carboidrato": float(self.campos["carboidrato"].get()),
                "gordura": float(self.campos["gordura"].get()),
            }
            self.controller.app.alterar_alimentos_usuario(alimento, "adicionar")
            for var in self.campos.values():
                var.set("")
            messagebox.showinfo("Sucesso", f"Alimento '{alimento['nome']}' cadastrado!")
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")


# ===================== ATUALIZAR PERFIL =====================

class AtualizarPerfilPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="Atualizar Perfil", font=("Helvetica", 16, "bold")).pack(pady=(10, 15))

        form = ttk.Frame(self)
        form.pack()

        self.campos = {}
        labels = [("Sexo (m/f)", "sexo"), ("Idade", "idade"), ("Peso (kg)", "peso"), ("Altura (cm)", "altura")]

        for i, (label, key) in enumerate(labels):
            ttk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="w", pady=3, padx=(0, 10))
            var = tk.StringVar()
            ttk.Entry(form, textvariable=var, width=25).grid(row=i, column=1, pady=3)
            self.campos[key] = var

        row_offset = len(labels)

        ttk.Label(form, text="Objetivo:").grid(row=row_offset, column=0, sticky="w", pady=3, padx=(0, 10))
        self.objetivo_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.objetivo_var, width=23, state="readonly",
                     values=["perda de peso", "manutenção", "ganho de massa"]).grid(row=row_offset, column=1, pady=3)

        ttk.Label(form, text="Nível de Atividade:").grid(row=row_offset + 1, column=0, sticky="w", pady=3, padx=(0, 10))
        self.nivel_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.nivel_var, width=23, state="readonly",
                     values=["sedentario", "leve", "moderado", "intenso", "muito intenso"]).grid(row=row_offset + 1, column=1, pady=3)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Salvar", command=self._salvar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("DashboardPage")).grid(row=0, column=1, padx=5)

    def ao_exibir(self):
        u = self.controller.app.usuario_logado
        self.campos["sexo"].set(u.sexo)
        self.campos["idade"].set(str(u.idade))
        self.campos["peso"].set(str(u.peso))
        self.campos["altura"].set(str(u.altura))
        self.objetivo_var.set(u.objetivo)
        self.nivel_var.set(u.nivel_atividade)

    def _salvar(self):
        u = self.controller.app.usuario_logado
        dados = {}
        try:
            sexo = self.campos["sexo"].get().strip()
            if sexo and sexo != u.sexo:
                dados["sexo"] = sexo

            idade = self.campos["idade"].get().strip()
            if idade and int(idade) != u.idade:
                dados["idade"] = int(idade)

            peso = self.campos["peso"].get().strip()
            if peso and float(peso) != u.peso:
                dados["peso"] = float(peso)

            altura = self.campos["altura"].get().strip()
            if altura and float(altura) != u.altura:
                dados["altura"] = float(altura)

            objetivo = self.objetivo_var.get()
            if objetivo and objetivo != u.objetivo:
                dados["objetivo"] = objetivo

            nivel = self.nivel_var.get()
            if nivel and nivel != u.nivel_atividade:
                dados["nivel_atividade"] = nivel

            if dados:
                self.controller.app.atualizar_usuario(dados)
                messagebox.showinfo("Sucesso", "Perfil atualizado!")
            else:
                messagebox.showinfo("Info", "Nenhuma alteração realizada.")

        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")


# ===================== HISTÓRICO DE CONSUMO =====================

class HistoricoPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="Histórico de Consumo", font=("Helvetica", 16, "bold")).pack(pady=(5, 10))

        self.meta_label = ttk.Label(self, text="", font=("Helvetica", 10))
        self.meta_label.pack(pady=(0, 5))

        # Área com scroll
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=20, pady=5)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.texto = tk.Text(text_frame, wrap="word", state="disabled", yscrollcommand=scrollbar.set,
                             font=("Courier", 10))
        self.texto.pack(fill="both", expand=True)
        scrollbar.config(command=self.texto.yview)

        ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("DashboardPage")).pack(pady=10)

    def ao_exibir(self):
        u = self.controller.app.usuario_logado
        consumo = u.consumo_diario
        meta = u.get

        self.meta_label.config(text=f"Meta diária (GET): {meta:.2f} kcal")

        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")

        if not consumo:
            self.texto.insert("end", "Nenhum consumo registrado.")
        else:
            for data in sorted(consumo.keys()):
                itens = consumo[data]
                total = sum(item[2] for item in itens)
                diff = total - meta

                if diff > 0:
                    status = f"acima da meta em {diff:.2f} kcal"
                elif diff < 0:
                    status = f"abaixo da meta em {abs(diff):.2f} kcal"
                else:
                    status = "na meta!"

                self.texto.insert("end", f"{data} — Total: {total:.2f} kcal ({status})\n")
                for item in itens:
                    self.texto.insert("end", f"   {item[0]} — {item[1]}g — {item[2]:.2f} kcal\n")
                self.texto.insert("end", "\n")

        self.texto.config(state="disabled")


# ===================== RELATÓRIO =====================

class RelatorioPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="Relatório Nutricional", font=("Helvetica", 16, "bold")).pack(pady=(5, 10))

        # Área com scroll
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=20, pady=5)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.texto = tk.Text(text_frame, wrap="word", state="disabled", yscrollcommand=scrollbar.set,
                             font=("Courier", 10))
        self.texto.pack(fill="both", expand=True)
        scrollbar.config(command=self.texto.yview)

        ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("DashboardPage")).pack(pady=10)

    def ao_exibir(self):
        u = self.controller.app.usuario_logado
        consumo = u.consumo_diario
        meta = u.get

        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")

        if not consumo:
            self.texto.insert("end", "Nenhum consumo registrado para gerar relatório.")
        else:
            dias = sorted(consumo.keys())
            totais = [sum(item[2] for item in consumo[d]) for d in dias]

            media = sum(totais) / len(totais)
            melhor_dia = dias[totais.index(min(totais, key=lambda t: abs(t - meta)))]
            dias_acima = sum(1 for t in totais if t > meta)
            dias_abaixo = sum(1 for t in totais if t < meta)

            self.texto.insert("end", f"{'=' * 50}\n")
            self.texto.insert("end", f"  RELATÓRIO NUTRICIONAL\n")
            self.texto.insert("end", f"{'=' * 50}\n\n")
            self.texto.insert("end", f"  Usuário:    {u.nome}\n")
            self.texto.insert("end", f"  Objetivo:   {u.objetivo}\n")
            self.texto.insert("end", f"  TMB:        {u.tmb:.2f} kcal\n")
            self.texto.insert("end", f"  GET (meta): {meta:.2f} kcal\n\n")
            self.texto.insert("end", f"  Período: {dias[0]} a {dias[-1]} ({len(dias)} dias)\n")
            self.texto.insert("end", f"{'-' * 50}\n\n")
            self.texto.insert("end", f"  Média diária consumida:  {media:.2f} kcal\n")
            self.texto.insert("end", f"  Dia mais próximo da meta: {melhor_dia}\n")
            self.texto.insert("end", f"  Dias acima da meta:  {dias_acima}\n")
            self.texto.insert("end", f"  Dias abaixo da meta: {dias_abaixo}\n\n")
            self.texto.insert("end", f"{'-' * 50}\n")
            self.texto.insert("end", f"  {'Data':<14} {'Calorias':>10}   {'Diferença':>12}\n")
            self.texto.insert("end", f"{'-' * 50}\n")

            for i, data in enumerate(dias):
                diff = totais[i] - meta
                sinal = "+" if diff >= 0 else ""
                self.texto.insert("end", f"  {data:<14} {totais[i]:>8.2f}   {sinal}{diff:>10.2f}\n")

            self.texto.insert("end", f"\n{'=' * 50}\n")

        self.texto.config(state="disabled")
