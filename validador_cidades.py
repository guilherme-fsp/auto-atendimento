import os
import json
import unidecode
from rapidfuzz import process, fuzz

class ValidadorCidades:
    def __init__(self, caminho_json="cidades.json"):
        caminho = os.path.join(os.path.dirname(__file__), caminho_json)
        with open(caminho, encoding="utf-8-sig") as f:
            self.cidades_json = json.load(f)
            self.todas_cidades = [c["nome"] for c in self.cidades_json]
            self.cidades_normalizadas = {
                self.normalizar(nome): nome for nome in self.todas_cidades
            }

    def normalizar(self, texto):
        return unidecode.unidecode(texto.strip().lower())

    def cidade_valida(self, entrada):
        texto = self.normalizar(entrada)
        resultados = []

        match_sort, score_sort, _ = process.extractOne(
            texto, list(self.cidades_normalizadas.keys()),
            scorer=fuzz.token_sort_ratio
        )
        resultados.append((match_sort, score_sort))

        match_partial, score_partial, _ = process.extractOne(
            texto, list(self.cidades_normalizadas.keys()),
            scorer=fuzz.partial_ratio
        )
        resultados.append((match_partial, score_partial))

        melhor = max(resultados, key=lambda x: x[1])
        if melhor[1] >= 85:
            return self.cidades_normalizadas[melhor[0]]
        return None

    def parecido(self, a, b, threshold=80):
        return fuzz.partial_ratio(a.lower(), b.lower()) >= threshold
