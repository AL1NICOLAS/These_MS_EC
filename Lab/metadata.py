import qrcode

# Données du QR code
data = "Hello, World!"

# Métadonnées supplémentaires
metadata = {
    "author": "John Doe",
    "date_created": "2022-01-01",
    "location": "Paris, France"
}

# Formatage des métadonnées en texte
metadata_text = '\n'.join(f"{key}: {value}" for key, value in metadata.items())

# Concaténation des données et des métadonnées
data_with_metadata = f"{data}\n{metadata_text}"

# Génération du QR code
qr = qrcode.QRCode()
qr.add_data(data_with_metadata)
qr.make()

# Sauvegarde du QR code en fichier image
qr_image = qr.make_image(fill_color="black", back_color="white")
qr_image.save("qrcode_with_metadata.png")
