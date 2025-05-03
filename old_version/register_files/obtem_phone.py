import requests
request_data = {
  "fields": "id,cc,country_dial_code,display_phone_number,verified_name,status,quality_rating,search_visibility,platform_type,code_verification_status",
  "access_token": "EAAJQdclr2Q4BOZBsmPRwCJB49lHTwf5YFnnCDN7rT9RNPRJSoZBbBx6BZBr4jNKn8pdZAJeBNaCIK4NGNsfZCBnMS7gjVk7kONI5sLtcZA7WQWCK0gXSkBjzvi8Jb7ZCwStxnvNFLNcRyo6hp7qXZC4uVSIC5vRjACKQz0BYYaGFrPeX0pYevNpD6ZBX8lJPlZAOxMaSXvNtlMw37SBmgXjijvHhBOoLZBwCfT9lgwpryvv"
}
url = "https://graph.facebook.com/v22.0/9301335293316201/phone_numbers"
response = requests.get(url, params=request_data)
print(response.json())