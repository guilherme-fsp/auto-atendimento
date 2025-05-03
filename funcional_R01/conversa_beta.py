from datetime import datetime
from validador_cidades import ValidadorCidades

validador = ValidadorCidades()

arvore = {
    "menu": {
        "resposta": "Como posso ajudar?\n1 - Horário\n2 - Preços\n3 - Atendente",
        "opcoes": {
            "1": "horario",
            "2": "preco",
            "3": "atendente"
        }
    },
    "horario": {
        "resposta": "Nosso horário é das 9h às 18h, {nome}.\n0 - Voltar ao menu"
    },
    "preco": {
        "resposta": "Temos os seguintes planos, {nome}:\n2 - Plano Mensal\n3 - Plano Anual\n0 - Voltar ao menu",
        "opcoes": {
            "2": "mensal",
            "3": "anual",
            "0": "menu"
        }
    },
    "mensal": {
        "resposta": "O plano mensal custa R$ 99,90/mês. Deseja contratar?\n0 - Voltar"
    },
    "anual": {
        "resposta": "O plano anual custa R$ 999,00/ano. Com 2 meses grátis!\n0 - Voltar"
    },
    "atendente": {
        "resposta": "{nome}, por favor, envie sua dúvida. Um atendente responderá em breve."
    },
    "encerrar": {
        "resposta": "Ok, {nome}. A conversa foi encerrada. Quando precisar, estamos por aqui. 😊"
    }
}

estado_usuario = {}

def saudacao_dinamica():
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def processar_mensagem(mensagem, telefone, nome):
    mensagem = mensagem.strip().lower()

    # Força início do fluxo para novo contato ou após encerramento
    if telefone not in estado_usuario or estado_usuario[telefone] == "encerrar":
        estado_usuario[telefone] = "inicio"
        saudacao = saudacao_dinamica()
        return f"{saudacao}, {nome}! Nos informe sua cidade para darmos continuidade ao atendimento."

    # Confirmação da cidade
    if isinstance(estado_usuario[telefone], dict) and estado_usuario[telefone].get("estado") == "confirmar_cidade":
        if mensagem == "1":
            cidade = estado_usuario[telefone]["dados"]["cidade_sugerida"]
            estado_usuario[telefone] = {
                "estado": "menu",
                "dados": {"cidade": cidade}
            }
            return f"Perfeito, {nome}! Atendimento para {cidade} iniciado.\n\n{arvore['menu']['resposta']}"
        elif mensagem == "2":
            estado_usuario[telefone] = "inicio"
            return "Sem problemas! Por favor, digite novamente o nome da sua cidade."
        else:
            return "Por favor, responda com 1 para confirmar ou 2 para digitar novamente a cidade."

    # Coleta da cidade no início
    if estado_usuario[telefone] == "inicio":
        cidade = validador.cidade_valida(mensagem)
        if not cidade:
            return "Desculpe, não reconhecemos essa cidade. Pode tentar novamente digitando o nome corretamente?"

        estado_usuario[telefone] = {
            "estado": "confirmar_cidade",
            "dados": {"cidade_sugerida": cidade}
        }
        return f"Você quis dizer **{cidade}**, está correto?\n1 - Sim\n2 - Não"

    # Estado do menu principal
    if isinstance(estado_usuario[telefone], dict):
        estado_atual = estado_usuario[telefone].get("estado")
        dados = estado_usuario[telefone].get("dados", {})
    else:
        estado_atual = estado_usuario[telefone]
        dados = {}

    if mensagem == "0":
        estado_usuario[telefone] = {
            "estado": "menu",
            "dados": dados
        }
        return arvore["menu"]["resposta"]

    if mensagem == "9":
        estado_usuario[telefone] = "encerrar"
        return arvore["encerrar"]["resposta"].format(nome=nome)

    no = arvore.get(estado_atual, arvore["menu"])

    if "opcoes" in no and mensagem in no["opcoes"]:
        proximo = no["opcoes"][mensagem]
        estado_usuario[telefone] = {
            "estado": proximo,
            "dados": dados
        }
        return arvore[proximo]["resposta"].format(nome=nome)

    if estado_atual == "atendente":
        return f"Obrigado, {nome}. Sua mensagem foi registrada. Um atendente responderá em breve."

    if estado_atual in ["mensal", "anual"]:
        for termo in ["quero", "contratar", "sim", "isso", "claro"]:
            if termo in mensagem:
                return f"Ótimo, {nome}! Um atendente entrará em contato para finalizar a contratação do plano {estado_atual}."

    return f"Desculpe, {nome}, não entendi sua resposta. Por favor, escolha uma opção válida ou digite 0 para voltar ao menu."
