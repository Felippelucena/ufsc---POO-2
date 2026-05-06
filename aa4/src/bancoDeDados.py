import json
import os

'''
Classe BancoDeDados
Persistência em JSON dentro da pasta ./db/.
Métodos:
carregar_dados(filename): Carrega lista/dict do arquivo. Retorna [] se não existir.
salvar_dados(filename, data): Grava data em ./db/{filename}.json.
registrar_vitoria(resumo): Adiciona um registro à lista de ranking.
listar_ranking(top=10): Retorna os top resultados ordenados por fichas finais.
'''


class BancoDeDados:
    @classmethod
    def _caminho(cls, filename):
        return f'./db/{filename}.json'

    @classmethod
    def carregar_dados(cls, filename):
        caminho = cls._caminho(filename)
        if not os.path.exists(caminho):
            return []
        try:
            with open(caminho, 'r', encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"O arquivo {filename}.json contém dados inválidos.")

    @classmethod
    def salvar_dados(cls, filename, data):
        os.makedirs('./db', exist_ok=True)
        caminho = cls._caminho(filename)
        try:
            with open(caminho, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Erro ao salvar dados em {filename}.json: {e}")

    @classmethod
    def registrar_vitoria(cls, resumo: dict):
        if not isinstance(resumo, dict):
            raise ValueError("O resumo deve ser um dicionário.")
        ranking = cls.carregar_dados('ranking')
        if not isinstance(ranking, list):
            ranking = []
        ranking.append(resumo)
        cls.salvar_dados('ranking', ranking)

    @classmethod
    def listar_ranking(cls, top=10):
        ranking = cls.carregar_dados('ranking')
        if not isinstance(ranking, list):
            return []
        ordenado = sorted(ranking, key=lambda r: r.get('fichas_finais', 0), reverse=True)
        return ordenado[:top]
