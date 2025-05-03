import requests

ACCESS_TOKEN = "EAAJQdclr2Q4BO8ZCJLoqStGW0dXMKd2zZBczNESMOKcRcy3p4NLk5SOtF997PtPiHs8TQpNEvEuIEAe5cIqF6dquaoLYoad8T8PKI7SrsNjfeGOxUn4WQ0paIocQyOtqpIuQ8GjyZA0ROyRvc9phBh4jIZBx3Mkb2EAurktCD2Klgu8I968U9olJOjhNJicr8Xna6vZB4RZApC9e96gAywj65CeCJPfbcZCbHAHZCWKH"
PHONE_NUMBER_ID = "582046188327185"
WHATSAPP_NUMBER = "5521996483573"

url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": WHATSAPP_NUMBER,
    "type": "template",
    "template": {
        "name": "hello_world",  # nome EXATO, minúsculo, sem espaços
        "language": {
            "code": "en_us"
        },
        
    }
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("✅ Template enviado com sucesso!")
else:
    print(f"❌ Erro ao enviar: {response.text}")