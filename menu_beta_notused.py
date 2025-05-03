
from datetime import datetime
from rapidfuzz import fuzz, process
import json
import os
import unidecode


#Carrega as cidades brasileiras de um json
caminho = os.path.join(os.path.dirname(__file__), "cidades.json")

with open(caminho, encoding="utf-8-sig") as f:
    cidades_json = json.load(f)
    todas_cidades = [c["nome"] for c in cidades_json]


#função de fuzzy matching para achar o que foi digitado mesmo se errado
def parecido(a, b, threshold=80):
    return fuzz.partial_ratio(a.lower(), b.lower()) >= threshold

#função de validação da cidade na entrada
def normalizar(texto):
    return unidecode.unidecode(texto.strip().lower())

def cidade_valida(input_text):
    texto = normalizar(input_text)
    cidades_normalizadas = {normalizar(cidade): cidade for cidade in todas_cidades}
    match, score, _ = process.extractOne(
        texto,
        list(cidades_normalizadas.keys()),
        scorer=fuzz.ratio
    )
    return cidades_normalizadas[match] if score >= 85 else None



arvore = {
    "inicio": {
        "resposta": """{saudacao}, {nome}! Nos informe sua cidade para darmos continuidade ao atendimento.
1 - Horário
2 - Preços
3 - Atendente
""",
        "opcoes": {
            "1": "Horario",
            "2": "Preco",
            "3": "Atendente",
            
        }
    },
    "Horario": {
        "resposta": """Nosso horário é das 9h às 18h, {nome}.
0 - Voltar ao início"""
    },
    "preco": {
        "resposta": """Temos os seguintes planos, {nome}:
2 - Plano Mensal
3 - Plano Anual
0 - Voltar ao início""",
        "opcoes": {
            "2": "Mensal",
            "3": "Anual",
            "0": "Inicio"
        }
    },
    "Mensal": {
        "resposta": """O plano mensal custa R$ 99,90/mês. Deseja contratar?
0 - Voltar"""
    },
    "Semestral": {
        "resposta": """O plano anual custa R$ 999,00/ano. Com 2 meses grátis!
0 - Voltar"""
    },
        "Anual": {
        "resposta": """O plano anual custa R$ 999,00/ano. Com 2 meses grátis!
0 - Voltar"""
    },

    "atendente": {
        "resposta": """{nome}, por favor, envie sua dúvida. Um atendente responderá em breve."""
    },
    "encerrar": {
        "resposta": """Ok, {nome}. A conversa foi encerrada. Quando precisar, estamos por aqui. 😊"""
    }
}

estado_usuario = {}


#saudação baseada na hora da mensagem enviada
def saudacao_dinamica():
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def processar_mensagem(mensagem, telefone, nome):
    estado_atual = estado_usuario.get(telefone, "inicio")
    no = arvore.get(estado_atual, arvore["inicio"])

    mensagem = mensagem.strip().lower()


    #Força o inicio do fluxo de conversa
    if telefone not in estado_usuario or estado_usuario[telefone] == "encerrar":
        estado_usuario[telefone] = "inicio"
        saudacao = saudacao_dinamica()
        return arvore["inicio"]["resposta"].format(nome=nome, saudacao=saudacao)
    

    if estado_usuario.get(telefone) == "inicio":
        cidade = cidade_valida(mensagem)
        if not cidade:
            return "Desculpe, não reconhecemos essa cidade. Pode tentar novamente digitando o nome corretamente?"

        estado_usuario[telefone] = {
            "estado": "menu",
            "dados": {"cidade": cidade}
            }
        return f"Perfeito, {nome}! Atendimento para {cidade} iniciado.\n\nComo posso ajudar?\n1 - Horário\n2 - Preços\n3 - Atendente\n"

    if mensagem == "0":
        estado_usuario[telefone] = "inicio"
        saudacao = saudacao_dinamica()
        return arvore["inicio"]["resposta"].format(nome=nome, saudacao=saudacao)

    #if mensagem == "9":
        estado_usuario[telefone] = "encerrar"
        return arvore["encerrar"]["resposta"].format(nome=nome)

    if "opcoes" in no and mensagem in no["opcoes"]:
        proximo = no["opcoes"][mensagem]
        estado_usuario[telefone] = proximo
        return arvore[proximo]["resposta"].format(nome=nome)

    if estado_atual == "atendente":
        return f"Obrigado, {nome}. Sua mensagem foi registrada. Um atendente responderá em breve."
    

    if estado_atual in ["mensal", "anual"]:
        for termo in(palavra in mensagem for palavra in ["quero", "contratar", "sim", "isso", "claro",]):
            if parecido(mensagem, termo):
                return f"Ótimo, {nome}! Um atendente entrará em contato para finalizar a contratação do plano {estado_atual}."
    
    return f"Desculpe, {nome}, não entendi sua resposta. Por favor, escolha uma opção válida ou digite 0 para voltar ao início."
