from flask import Flask, request, jsonify, render_template
#from conversa import processar_mensagem
from conversa_beta import processar_mensagem
from collections import defaultdict
import requests

app = Flask(__name__)


VERIFY_TOKEN = "ielogSPa-bA2xSS_2CE6OxWitRDIxQVFLWRHwOoBqYA"
ACCESS_TOKEN = "EAAJQdclr2Q4BOZBsmPRwCJB49lHTwf5YFnnCDN7rT9RNPRJSoZBbBx6BZBr4jNKn8pdZAJeBNaCIK4NGNsfZCBnMS7gjVk7kONI5sLtcZA7WQWCK0gXSkBjzvi8Jb7ZCwStxnvNFLNcRyo6hp7qXZC4uVSIC5vRjACKQz0BYYaGFrPeX0pYevNpD6ZBX8lJPlZAOxMaSXvNtlMw37SBmgXjijvHhBOoLZBwCfT9lgwpryvv"  # seu token
PHONE_NUMBER_ID = "624913207365243"

#Lista para guardar historico de mensagens

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
        messages = value.get('messages')
        nome = value['contacts'][0]['profile']['name'] if 'contacts' in value else "amigo(a)"
        
        if messages:
            msg = messages[0]
            text = msg['text']['body']
            sender = msg['from']
            
            client_id = f"{nome} ({sender})"

            print(f"👤 {sender} ({nome}) disse: {text}")

            resposta = processar_mensagem(text, sender, nome)
            enviar_mensagem(sender, resposta)

                        # Salvar no histórico
            conversas.append({
                "remetente": client_id,
                "recebido": text,
                "resposta": resposta
            })

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


#rota pro historico.html
@app.route('/', methods=['GET'])
def hist():
    agrupadas = defaultdict(list)
    for c in conversas:
        agrupadas[c['remetente']].append(c)

    return render_template("historico.html", conversas_por_numero=agrupadas)


#rota pro home.html
@app.route('/home')
def home_page():
    return render_template("home.html")



if __name__ == '__main__':
    app.run(port=5000, debug=True)
