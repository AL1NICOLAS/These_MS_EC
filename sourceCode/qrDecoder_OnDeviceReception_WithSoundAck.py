# =======================
#  Author : Alain NICOLAS
# =======================
# Ce programme permet de lire et décoder les QrCodes affichés par la device Source.
# Lorsque le QRCode est lu et décodé, la data en est extraite et mise en liste puis
# Un son particulier est émis par le programme dans le but d'être capté et analysé
# par le programme afficheur sur la device source qui affichera le QRCode suivant.
# Le QRCode véhicule son rang dans la collection.
# Lorsque tous les QRCodes sont reçus, les datas sont concaténées et décodées de la base4 pour
# restituer le payload binaire tar.gz.

import cv2
import pygame
import time
import base64
from pyzbar import pyzbar
import logging
from urllib.parse import quote
import os

# Initialiser pygame
pygame.mixer.init()
# Charger le son du bip
son_bip = pygame.mixer.Sound("./laserbip.wav")

# Initialisation de la liste contenant les données unitaires à rassembler
listDecDatas = []

# Initialiser la capture vidéo à partir de la webcam (0 --> webcam intégrée, 2 ou 4 pour webcams usb)
capture = cv2.VideoCapture(4)

#  CONSTANTES environnement
#  ========================
PATH_ROOT = "/home/lanig/PycharmProjects/ThèseProUttMS_EFC"
FOLDER_LOG = f"{PATH_ROOT}/logs"
FILE_LOG = "/qrDecodeurWithSoundAck_errors.log"
FOLDER_TMP = f"{PATH_ROOT}/temp"
OUTPUT_FILE_TAR_GZ = f"{PATH_ROOT}/decodedOut/datasLeakOut.tar.gz"
url_fichier_tar_gz =f"{OUTPUT_FILE_TAR_GZ}"
encoded_url = quote(url_fichier_tar_gz)
# liste contenant tous les qrcodes part
list_qrcodes = []

# Configurer le journal des erreurs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=FOLDER_LOG + FILE_LOG, level=logging.ERROR)

# Récupérer le nom du programme Python en cours d'exécution
nom_programme = os.path.basename(__file__)
print(f"\n\033[1m\033[4mNom du programme: \033[32m {nom_programme}\033[0m \n")

def save_qr_data_to_step_file(qr_data, output_file):
    data64 = ''
    for data_dec in qr_data:
        data64 = data64 + data_dec
    with open(output_file, "wb") as fileBinary:
        fileBinary.write(base64.b64decode(data64))


if __name__ == '__main__':
    try:
        start_time = time.time()
        # Init variable pour Test continuité de séquence
        list_qrcodes = []
        list_dec_datas = []
        num_seq_attendue = 1
        num_seq_qr = ' '
        num_seq_max = ''
        while True:
            # Lire une image depuis la webcam
            ret, frame = capture.read()

            # Convertir l'image en échelle de gris
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Détecter les codes QR dans l'image
            barcodes_pyz = pyzbar.decode(gray)
            print(len(barcodes_pyz))

            # Parcourir les codes QR détectés
            if len(barcodes_pyz):
                for qr_code in barcodes_pyz:
                    if qr_code.type == "QRCODE":
                        try:
                            qrcode_data = qr_code.data.decode("utf-8")
                            qr_meta_data, data = qrcode_data.split('\n', 1)
                            # Affichage des données et des métadonnées
                            num_seq_qr, num_seq_max = qr_meta_data.split('/', 1)
                            print(f"Métadonnées : -{num_seq_qr}-/-{num_seq_max}-{num_seq_attendue}-")
                            if int(num_seq_qr) == num_seq_attendue:
                                num_seq_attendue += 1
                                print(f"num_seq_attendue==> {num_seq_attendue}")
                                # Sauvegarde des qrcodes détectés dans la liste list_qrcodes
                                list_qrcodes.append(qr_code)
                                # Jouer le son du bip lorsque le code QR est détecté
                            son_bip.play()
                        except Exception as e:
                            logging.exception("Une erreur s'est produite lors de la détection des QR codes : ", e)
            # Quitter la boucle si la touche 'q' est pressée ou si la séquence est terminée
            if (cv2.waitKey(1) & 0xFF == ord('q')) or (num_seq_qr == num_seq_max):
                break

        # Décoder le contenu du code QR en sortie de boucle
        for qrcode in list_qrcodes:
            try:
                qrcode_payload = qrcode.data.decode("utf-8")
                qrcode_type = qrcode.type
                metadata, qr_data64 = qrcode_payload.split('\n', 1)
                # Afficher le contenu du code QR
                if qrcode_type == "QRCODE":
                    if qr_data64 not in list_dec_datas:
                        list_dec_datas.append(qr_data64)
            except Exception as e:
                logging.exception("Une erreur s'est produite lors du décodage du code QR : ", e)

        # Enregistrer les données dans un fichier STEP
        save_qr_data_to_step_file(list_dec_datas, OUTPUT_FILE_TAR_GZ)

        # Libérer les ressources
        capture.release()
        cv2.destroyAllWindows()

        # Affichage Fin de traitement
        print(f"\nFin du traitement de décodage et ré-assemblage.")
        print(f"==> Emplacement de l'archive tar.gz sur le disque : file://{encoded_url}")
        end_time = time.time()
        duration = round((end_time - start_time), 3)
        print(f"\nDurée de traitement : \033[93m {duration}\033[0m seconde(s)")
    except Exception as e:
        logging.exception("Une erreur s'est produite lors de l'exécution du programme : ", e)
