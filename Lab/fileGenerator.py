import random

def generate_file(file_path, file_size):
    with open(file_path, 'wb') as file:
        bytes_to_write = file_size
        while bytes_to_write > 0:
            # Générer des données aléatoires de taille maximale 4096 bytes
            data = bytearray(random.getrandbits(8) for _ in range(min(bytes_to_write, 4096)))
            file.write(data)
            bytes_to_write -= len(data)

# Appel de la fonction pour générer un fichier de 1 Mo
generate_file('../in_files_to_exfiltrate/output.txt', 1024 * 1024)
