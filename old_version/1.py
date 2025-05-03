import requests
# Defina os dados da API do WhatsApp
ACCESS_TOKEN = "EAAJQdclr2Q4BOxIkgvZBTlpb5bMI7o9457DZCJHKaeVoZAKIGsIIcUzmttSZB6LXfio6pQRInsC39BnRWHV3XRcZCIp62jKS116B5MYoGgTFknmsmZAgtS54xQt6F6zZASPz8efA7S6g67n1ZCqCFa2ajX32dkBZAuEO11GWpGf4RTr2d3K01wIqB7tx1ZCmSrwpZBK7VyKeIizkNQGrO5FWJlgpxPwGqEKPYxkzUsjloszFgZDZD"  # Substitua pelo seu token gerado pela Meta
PHONE_NUMBER_ID = "582046188327185"  # O ID do seu número no WhatsApp Business
WHATSAPP_NUMBER = "5521996483573"  # Número de destino no formato internacional

# URL da API do WhatsApp
url = f"https://graph.facebook.com/v22.0/582046188327185/messages"

# Cabeçalhos da requisição
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Corpo da mensagem
data = {
    "messaging_product": "whatsapp",
    "to": WHATSAPP_NUMBER,
    "type": "template",
    "template": {
        "name": "teste2",  # Nome exato do seu template aprovado
        "language": {
            "code": "pt_BR"  # ou en_US, dependendo do que foi aprovado
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": "Arthur"  # valor da variável {{1}} no template
                    }
                ]
            }
        ]
    }
}

# Fazendo a requisição HTTP POST
response = requests.post(url, json=data, headers=headers)

# Verificando a resposta
if response.status_code == 200:
    print("✅ Mensagem enviada com sucesso!")
else:
    print(f"❌ Erro ao enviar mensagem: {response.text}")

print(f"📌 Código HTTP: {response.status_code}")
print(f"📌 Resposta da API: {response.text}")