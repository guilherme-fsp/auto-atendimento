import requests
from flask import Flask, request

app = Flask(__name__)

# O mesmo token que você colocou no Facebook Developer
VERIFY_TOKEN = "ielogSPa-bA2xSS_2CE6OxWitRDIxQVFLWRHwOoBqYA"
ACCESS_TOKEN = "EAAJQdclr2Q4BO3xZAg5lF0YnYzafEITQsZBN7iSgZBxYCPZAbUK0367gWKnlZBJFtypzJfGcUhw9fgUza19CDE7Px0JD9wRZBeOZB0shyYZAsCGB2AKbri4tkbKMPONhSurevnDK8v6WDXDpgK3YTtcITFSWobOQQNqiZCPWReCVaez7ZAHrPw45twsJPZCo41AFlZCJqQZDZD"
PHONE_NUMBER_ID = "624913207365243"

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verifica se o Webhook do Facebook está configurado corretamente."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verificado com sucesso!")
        return challenge, 200

    print("❌ Erro na verificação do Webhook")
    return "Erro na verificação", 403

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Recebe mensagens do WhatsApp e responde automaticamente."""
    data = request.json  # Captura os dados recebidos
    print("📩 Mensagem recebida:", data)

    # Verifica se é uma mensagem de texto do WhatsApp
    if "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    for message in value["messages"]:
                        sender_id = message["from"]  # ID do remetente (número do WhatsApp)
                        message_text = message.get("text", {}).get("body", "").lower()

                        # Defina uma resposta personalizada
                        response_text = process_message(message_text)

                        # Enviar resposta automática
                        send_whatsapp_message(sender_id, response_text)

    return {"status": "success"}, 200

def process_message(message_text):
    """Processa a mensagem recebida e gera uma resposta."""
    if "oi" in message_text or "olá" in message_text:
        return "Olá! Como posso ajudar você? 😊"
    elif "horário" in message_text:
        return "Nosso horário de atendimento é das 9h às 18h."
    elif "preço" in message_text:
        return "Os valores variam conforme o serviço. Entre em contato para mais detalhes."
    else:
        return "Desculpe, não entendi. Você pode reformular sua pergunta?"

def send_whatsapp_message(to, text):
    """Envia uma mensagem para o WhatsApp."""
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)