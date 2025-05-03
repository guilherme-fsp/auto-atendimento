import requests
request_data = {
  "fields": "id,name,currency,owner_business_info",
  "limit": 20,
  "access_token": "EAAJQdclr2Q4BOZBsmPRwCJB49lHTwf5YFnnCDN7rT9RNPRJSoZBbBx6BZBr4jNKn8pdZAJeBNaCIK4NGNsfZCBnMS7gjVk7kONI5sLtcZA7WQWCK0gXSkBjzvi8Jb7ZCwStxnvNFLNcRyo6hp7qXZC4uVSIC5vRjACKQz0BYYaGFrPeX0pYevNpD6ZBX8lJPlZAOxMaSXvNtlMw37SBmgXjijvHhBOoLZBwCfT9lgwpryvv"
}
url = "https://graph.facebook.com/v22.0/624032780250698/owned_whatsapp_business_accounts"
response = requests.get(url, params=request_data)
print(response.json())
