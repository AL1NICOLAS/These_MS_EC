import base64

data = b'Hello, World!'  # Chaîne de caractères binaire
base64_encoded = base64.b64encode(data)  # Encodage en base64

base64_str = base64_encoded.decode()  # Conversion en chaîne de caractères Unicode
print(base64_encoded)
