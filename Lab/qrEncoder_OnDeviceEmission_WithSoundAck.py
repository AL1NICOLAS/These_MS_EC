# Author : Alain NICOLAS
# Ce programme permet de rassembler les pièces numériques à exfiltrer
# Après avoir constitué une archive qui ensuite est compressée, le binaire
# du zip est  encodé en base64. L'information base64 est découpée afin de générer
#  autant de QRCodes que nécessaires :
#    -
import base64
import shutil
import tarfile
import segno
import logging
import os

# CONSTANTES environnement
PATH_ROOT = "/"
FOLDER_IN = f"{PATH_ROOT}/decodedIn"
FOLDER_QR = f"{PATH_ROOT}/encoded"
FOLDER_LOG = f"{PATH_ROOT}/logs"
OUTPUT_TAR_FILENAME = f"{PATH_ROOT}/temp/exFiles.tar.gzip"

# Configurer le journal des erreurs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename=FOLDER_LOG + '/encoderD2Q_errors.log',
                    level=logging.ERROR)


def create_tar(fold_in, fold_out):
    try:
        with tarfile.open(fold_out, "w:gz") as tar:
            tar.add(fold_in, arcname="")  # Ajouter l'ensemble du répertoire à l'archive tar
    except Exception as err1:
        logging.error(f"Erreur lors de la création de l'archive tar : {err1}")


def vider_repertoire(path):
    try:
        if os.path.isdir(path):  # Supprimer récursivement tous les fichiers et sous-répertoires
            shutil.rmtree(path)
            # Recréer le répertoire vide
            os.mkdir(path)
        else:
            # Recréer le répertoire vide
            os.mkdir(path)
    except Exception as err2:
        logging.error(f"Erreur lors de la suppression du répertoire : {err2}")


if __name__ == '__main__':

    try:
        # Utilisation de la fonction vider_repertoire pour initialiser l'environnement
        vider_repertoire(FOLDER_QR)
        # Tar&zip des données à exfiltrer
        create_tar(FOLDER_IN, OUTPUT_TAR_FILENAME)

        with open(OUTPUT_TAR_FILENAME, "rb") as f:
            # Découpage du contenu du fichier à exfiltrer en plusieurs parties de taille fixe
            # Taille de découpage de la data encodée b64 (en caractères) contenue dans chaque QRCode
            # Directement liée à la qualité de la correction d'erreur choisie (segno.make_qr)
            part_size = 2950
            fileContent = f.read()
            # Convertir les données du fichier ZIP en base64
            fileContentBase64 = base64.b64encode(fileContent).decode("utf-8")
            # Découpage pour constituer les codes QR
            parts = [fileContentBase64[i: i + part_size] for i in range(0, len(fileContentBase64), part_size)]

        # Génération des codes QR pour chaque partie
        qr_codes = []
        print(len(parts))
        for part in parts:
            qr_codes.append(segno.make_qr(part,
                                          # error='l',
                                          mode='byte',
                                          boost_error=True
                                          )
                            )  # Error correction level: “L”: 7% (default), “M”: 15%, “Q”: 25%, “H”: 30%, “-”
        for element in qr_codes:
            print("\n" + "QRK ==> " + str(element))

        # Enregistrement des codes QR sous forme d'images PNG
        for i, qr_code in enumerate(qr_codes):
            qr_code.save(f"{FOLDER_QR}/qr_code_part{i}.png",
                         # dark='#1B5E20',
                         # dark='black',
                         # light='white',
                         # data_dark='#1B5E20',
                         # data_light='',
                         scale=3)

    except Exception as err3:
        logging.error(f"Une erreur s'est produite dans le traitement main : {err3}")