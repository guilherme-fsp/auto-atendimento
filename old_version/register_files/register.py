import requests

url = "https://graph.facebook.com/v18.0/624913207365243/register"
headers = {
    "Authorization": "Bearer EAAJQdclr2Q4BOZBsmPRwCJB49lHTwf5YFnnCDN7rT9RNPRJSoZBbBx6BZBr4jNKn8pdZAJeBNaCIK4NGNsfZCBnMS7gjVk7kONI5sLtcZA7WQWCK0gXSkBjzvi8Jb7ZCwStxnvNFLNcRyo6hp7qXZC4uVSIC5vRjACKQz0BYYaGFrPeX0pYevNpD6ZBX8lJPlZAOxMaSXvNtlMw37SBmgXjijvHhBOoLZBwCfT9lgwpryvv",
    "Content-Type": "application/json"
}
data = {
    "messaging_product": "whatsapp",
    "cc": "55",
    "phone_number": "22999615513",
    "method": "sms"
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())