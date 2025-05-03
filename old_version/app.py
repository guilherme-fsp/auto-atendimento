import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "ielogSPa-bA2xSS_2CE6OxWitRDIxQVFLWRHwOoBqYA"
ACCESS_TOKEN = "EAAJQdclr2Q4BO2GoHP6FetAqlfR2gdPexBTUELPg9WN0JZBbYQVDdvNlBL2VtEoHtgPUZAuB12MTu5ZCwCDeZBqxHCyBpFGcIrS06CeJuHIGTgNUYTSXWKApwhRc3tU6zCB5SxZB3Hivb0xJZBZCrPrbUYKFLF666LIwuiBzxyU2tzOqZCPJd0rXuC9JXrdQCVUwJstCZAYxbiBuZBjnBOv8WAxXnH8JsZB2wl7Tz5YRHOI"  # seu token
PHONE_NUMBER_ID = "624913207365243"

@app.route('/webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        challenge = request.args.get('hub.challenge')
        incoming_token = request.args.get('hub.verify_token')

        if mode == 'subscribe' and incoming_token == VERIFY_TOKEN:
            print("🌟 Webhook verificado com sucesso!")
            return challenge, 200
        else:
            print("❌ Erro de verificação do Webhook")
            return "Erro de verificação", 403

    if request.method == 'POST':
        data = request.json
        print("📩 Mensagem recebida:", data)

        if "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value["messages"]:
                            sender_id = message["from"]
                            message_text = message.get("text", {}).get("body", "").lower()

                            # Processar a mensagem recebida
                            response_text = process_message(message_text)

                            # Enviar resposta automática
                            send_whatsapp_message(sender_id, response_text)

        return jsonify({"status": "success"}), 200

def process_message(message_text):
    if "Oi" in message_text or "olá" in message_text:
        return "Olá! Como posso ajudar você? 😊"
    elif "horário" in message_text:
        return "Nosso horário de atendimento é das 9h às 18h."
    elif "preço" in message_text:
        return "Os valores variam conforme o serviço. Entre em contato para mais detalhes."
    else:
        return "Desculpe, não entendi. Você pode reformular sua pergunta?"

def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("📤 Resposta enviada:", response.json())

@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head><title>Servidor WhatsApp Flask</title></head>
        <body>
            <h1>🚀 Servidor Flask rodando com sucesso!</h1>
            <p>Webhook ativo em /webhook</p>
        </body>
    </html>
    """, 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)
