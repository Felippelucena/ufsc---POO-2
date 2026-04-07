from src.bancoDeDados import BancoDeDados
from src.usuario import Usuario
from src.categoria import criar_categoria
from src.despesa import Despesa

class App:
    def __init__(self):
        self.categorias_padrao = BancoDeDados.carregar_dados('categorias_padrao')
        self.usuario_logado = None

    @property
    def usuario_logado(self):
        return self.__usuario_logado

    @usuario_logado.setter
    def usuario_logado(self, value):
        if value is not None and not isinstance(value, Usuario):
            raise ValueError("O usuário logado deve ser do tipo Usuario ou None.")
        self.__usuario_logado = value

    def adicionar_usuario(self, dados: dict):
        # Cria categorias padrão para o novo usuário
        categorias = {}
        for nome, limite in self.categorias_padrao.items():
            categorias[nome] = criar_categoria(nome=nome, limite=limite).json()
        dados['controle_financeiro'] = {"categorias": categorias}

        usuario = Usuario(**dados)
        BancoDeDados.adicionar_usuario(usuario)
        self.usuario_logado = usuario

    def entrar_usuario(self, nome: str):
        usuario = BancoDeDados.buscar_usuario(nome)
        if usuario:
            self.usuario_logado = usuario
            return True
        return False

    def atualizar_usuario(self, dados: dict):
        for k, v in dados.items():
            setattr(self.usuario_logado, k, v)
        BancoDeDados.atualizar_usuario(self.usuario_logado)

    def logout(self):
        BancoDeDados.atualizar_usuario(self.usuario_logado)
        self.usuario_logado = None

    def adicionar_despesa(self, despesa_dict: dict):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")

        despesa = Despesa(**despesa_dict)
        categoria_nome = despesa.categoria
        cf = self.usuario_logado.controle_financeiro

        if categoria_nome in cf.categorias:
            cf.categorias[categoria_nome].despesas = {"acao": "adicionar", **despesa.json()}
            BancoDeDados.atualizar_usuario(self.usuario_logado)

    def remover_despesa(self, categoria: str, indice: int):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")

        cf = self.usuario_logado.controle_financeiro
        if categoria in cf.categorias:
            cf.categorias[categoria].despesas = {"acao": "remover", "indice": indice}
            BancoDeDados.atualizar_usuario(self.usuario_logado)

    def definir_limite(self, categoria: str, limite: float):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")

        cf = self.usuario_logado.controle_financeiro
        if categoria in cf.categorias:
            cf.categorias[categoria].limite = limite
            BancoDeDados.atualizar_usuario(self.usuario_logado)

    def relatorio_mensal(self, mes_ano: str):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")
        return self.usuario_logado.controle_financeiro.relatorio_mensal(mes_ano)

    def comparar_meses(self, mes1: str, mes2: str):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")
        return self.usuario_logado.controle_financeiro.comparar_meses(mes1, mes2)

    def verificar_alertas(self):
        if not self.usuario_logado:
            return []
        return self.usuario_logado.controle_financeiro.alertas()

    def exportar_pdf(self, mes_ano: str, caminho: str = None):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")

        from fpdf import FPDF

        if caminho is None:
            caminho = f'relatorio_{mes_ano.replace("/", "-")}.pdf'

        relatorio = self.relatorio_mensal(mes_ano)
        alertas = self.verificar_alertas()

        pdf = FPDF()
        pdf.add_page()

        # Título
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Relatorio Financeiro Residencial', ln=True, align='C')
        pdf.ln(5)

        # Info do usuário
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f'Usuario: {self.usuario_logado.nome} | Email: {self.usuario_logado.email}', ln=True)
        pdf.cell(0, 8, f'Periodo: {mes_ano}', ln=True)
        pdf.ln(5)

        # Cabeçalho da tabela
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(60, 8, 'Categoria', 1)
        pdf.cell(40, 8, 'Total (R$)', 1)
        pdf.cell(40, 8, 'Limite (R$)', 1)
        pdf.cell(40, 8, 'Status', 1)
        pdf.ln()

        # Dados
        pdf.set_font('Arial', '', 10)
        total_geral = relatorio.pop("TOTAL", 0)
        for nome, dados in relatorio.items():
            total = dados['total']
            limite = dados['limite']
            limite_str = f"{limite:.2f}" if limite else "---"
            if limite and total >= limite:
                status = "ACIMA"
            elif limite and total >= limite * 0.8:
                status = "ATENCAO"
            else:
                status = "OK"

            pdf.cell(60, 8, nome, 1)
            pdf.cell(40, 8, f'{total:.2f}', 1)
            pdf.cell(40, 8, limite_str, 1)
            pdf.cell(40, 8, status, 1)
            pdf.ln()

        # Total geral
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(60, 8, 'TOTAL', 1)
        pdf.cell(40, 8, f'{total_geral:.2f}', 1)
        pdf.cell(40, 8, '', 1)
        pdf.cell(40, 8, '', 1)
        pdf.ln(10)

        # Alertas
        if alertas:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, 'Alertas:', ln=True)
            pdf.set_font('Arial', '', 10)
            for alerta in alertas:
                pdf.cell(0, 7, f'  - {alerta}', ln=True)

        pdf.output(caminho)
        return caminho
