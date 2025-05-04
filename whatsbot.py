#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from conversa_beta import processar_mensagem, estado_usuario  # Certifique-se que essa variável esteja exportada
from rotas_frontend import frontend_bp
from registro_historico import salvar_conversa
import requests
from collections import defaultdict
import os
from dotenv import load_dotenv



load_dotenv()
app = Flask(__name__)
app.register_blueprint(frontend_bp)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # seu token
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Lista local de histórico (para visualização ao vivo)
conversas = []

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("🌟 Webhook verificado com sucesso!")
        return challenge, 200
    else:
        print("❌ Verificação falhou.")
        return "Erro de verificação", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Mensagem recebida:", data)

    try:
        value = data['entry'][0]['changes'][0]['value']
        nome = value['contacts'][0]['profile']['name'] if 'contacts' in value else "amigo(a)"
        messages = value.get('messages')

        if messages:
            msg = messages[0]
            text = msg['text']['body']
            sender = msg['from']
            resposta = processar_mensagem(text, sender, nome)

            salvar_conversa(
                numero=sender,
                nome=nome,
                cidade=estado_usuario.get(sender, {}).get("dados", {}).get("cidade", "Indefinida"),
                recebido=text,
                resposta=resposta,
                estado=estado_usuario.get(sender, {}).get("estado", "inicio"),
                msg_id=msg["id"]
            )

            enviar_mensagem(sender, resposta)

            client_id = f"{nome} ({sender})"
            conversas.append({
                "remetente": client_id,
                "recebido": text,
                "resposta": resposta
            })

            print(f"👤 {sender} ({nome}) disse: {text}")
    except Exception as e:
        print("Erro ao processar:", e)

    return jsonify({"status": "ok"}), 200

def enviar_mensagem(telefone, mensagem):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "text",
        "text": {"body": mensagem}
    }

    r = requests.post(url, json=payload, headers=headers)
    print("📤 Enviado:", r.status_code, r.text)

@app.route('/', methods=['GET'])
def hist():
    agrupadas = defaultdict(list)
    for c in conversas:
        agrupadas[c['remetente']].append(c)

    return render_template("historico.html", conversas_por_numero=agrupadas)

@app.route('/home')
def home_page():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)