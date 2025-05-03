import json
import os
from datetime import datetime

ARQUIVO = "conversas.json"

def carregar_conversas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_conversa(numero, nome, cidade, recebido, resposta, estado, msg_id):
    conversas = carregar_conversas()
    nova = {
        "numero": numero,
        "nome": nome,
        "cidade": cidade,
        "recebido": recebido,
        "resposta": resposta,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "estado": estado,
        "msg_id": msg_id
    }
    conversas.append(nova)

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(conversas, f, ensure_ascii=False, indent=2)