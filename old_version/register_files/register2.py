import requests

# Substitua isso pelo seu token de acesso válido
ACCESS_TOKEN = "EAAJQdclr2Q4BOZBsmPRwCJB49lHTwf5YFnnCDN7rT9RNPRJSoZBbBx6BZBr4jNKn8pdZAJeBNaCIK4NGNsfZCBnMS7gjVk7kONI5sLtcZA7WQWCK0gXSkBjzvi8Jb7ZCwStxnvNFLNcRyo6hp7qXZC4uVSIC5vRjACKQz0BYYaGFrPeX0pYevNpD6ZBX8lJPlZAOxMaSXvNtlMw37SBmgXjijvHhBOoLZBwCfT9lgwpryvv"

# ID do número de telefone que você obteve no painel do Facebook Developers
PHONE_NUMBER_ID = "624913207365243"

# URL da requisição para registrar o número
url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/register"

# Cabeçalhos da requisição
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Corpo da requisição (usando SMS como método de verificação)
data = {
    "messaging_product": "whatsapp",
    "cc": "55",
    "phone_number": "22999615513",  # sem o DDI
    "method": "sms",
    "cert": "Cm8KKwihvoD5tfbDAhIGZW50OndhIhJBcmVhZmFjaWwgU2Vydmljb3NQyrDFwAYaQNP3vFarNInABweHymYhk6mq+mYpGDvcgDrihmyGpKObSm9tuKCsjbRlk2ra4OHLlfYESjsURNSg7SjJwGIsrQ0SMG13K+ja5fvz4lqzt52ubyCcU+LkWcDxLl4GMY1NOtxeyDW7sFCOJCponPrbeYmkmg==",
    "pin": "123456"
}

# Envia a requisição
response = requests.post(url, headers=headers, json=data)

# Exibe o resultado
print(response.status_code)
print(response.json())