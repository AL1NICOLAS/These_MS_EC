# =======================
#  Author : Alain NICOLAS
# =======================
# Ce programme permet de lire et décoder les QrCodes"ACK" affichés par la device Source.
# Lorsque le QRCode est lu et décodé, la data en est extraite et mise en liste puis
# un QRCode d'acquittement contenant en data la séquence acquittée est généré et affiché
# dans le but d'être scanné, analysé et décodé par le programme afficheur sur la device source
# qui se synchronise et affiche le QRcode suivant.
# Le QRCode véhicule son rang dans la collection.
# Lorsque tous les QRCodes sont reçus, les datas sont concaténées et décodées de la base4 pour
# restituer le payload binaire tar.gz.
import logging
import os
import time
from urllib.parse import quote

import base45
import cv2
import pygame
import segno
from dotenv import load_dotenv
from pyzbar import pyzbar

load_dotenv()
PATTERN_SEP = os.getenv("PATTERN_SEP")

# Initialiser pygame
pygame.mixer.init()
# Charger le son du bip
son_bip = pygame.mixer.Sound("./laserbip.wav")


#  CONSTANTES environnement
#  ========================
PATH_ROOT = "/home/lanig/PycharmProjects/These_MS_EC"
FOLDER_LOG = f"{PATH_ROOT}/logs"
FILE_LOG = "/qrDecodeurWithQRAck_errors.log"
FOLDER_OUT = f"{PATH_ROOT}/decodedOut"
OUTPUT_FILE_TAR_GZ = f"{PATH_ROOT}/decodedOut/datasLeakOut.tar.gz"
url_fichier_tar_gz = f"{OUTPUT_FILE_TAR_GZ}"
encoded_url = quote(url_fichier_tar_gz)
PATTERN_SEP = os.getenv("PATTERN_SEP")

# variables paramétriques
# ========================
filename_ack_file_png = 'ack_qrcode_with_metadata.png'
# Configurer le journal des erreurs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=FOLDER_LOG + FILE_LOG, level=logging.INFO)

# Récupérer le nom du programme Python en cours d'exécution
nom_programme = os.path.basename(__file__)
print(f"\n\033[1m\033[4mNom du programme: \033[32m {nom_programme}\033[0m \n")

def is_folder_exist(repertoire):
    try:
        if os.path.isdir(repertoire):
            print(f"Le répertoire {repertoire} existe.")
        else:
            print(f"Le répertoire {repertoire} n'existait pas, il a été créé")
            os.mkdir(repertoire)
        if not os.path.isfile(FOLDER_LOG + FILE_LOG):
            # Création du fichier
            with open(FOLDER_LOG + FILE_LOG, 'w'):
                # Opérations sur le fichier, si nécessaire
                pass
                print(f"Le fichier {FILE_LOG} vide a été créé.")
    except Exception as err4:
        logging.error(f"Erreur lors de la création du répertoire {repertoire} : {err4}")

def save_qr_data_to_step_file(qr_data, output_file):
    data_parts = []
    for data_part in qr_data:
        data_parts.append(data_part)
    data_45 = ''.join(data_parts)
    with open(output_file, "wb") as fileBinary:
        fileBinary.write(base45.b45decode(data_45))


def make_qr_ack_pres(metadata_qr):
    # Génération du QR code
    qr_ack = segno.make_qr(metadata_qr, error="l")
    # Sauvegarde du QR code en fichier image
    qr_ack.save(filename_ack_file_png, scale=10)
    while True:
        qr_code_ack = cv2.imread(filename_ack_file_png)
        cv2.imshow("Device_MALVEILLANTE_RECEPTRICE_Afficheur_QRCodes_ACK", qr_code_ack)
        # Positionnement délai
        cv2.waitKey(2)
        #  # Déplacer la fenêtre à un emplacement spécifique de l'écran
        cv2.moveWindow("Device_MALVEILLANTE_RECEPTRICE_Afficheur_QRCodes_ACK", 2200, 300)  # Coordonnées x=100, y=100
        # Positionnement délai
        cv2.waitKey(3)
        return


def detector_qr_aff():
    while True:
        try:
            # Lire une image depuis la webcam
            ret, frame = capture.read()
            # Convertir l'image en échelle de gris
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Détecter les codes QR dans l'image
            qrcodes_pyz = pyzbar.decode(gray_frame)
            # print(len(qrcodes_pyz))
            # Parcourir les codes QR détectés
            if len(qrcodes_pyz):
                print(len(qrcodes_pyz))
                for qrcode in qrcodes_pyz:
                    # récupération de la seq lue
                    if qrcode.type == "QRCODE":  # sécurité contre les autres types que QRCODE (BARCODE)
                        print("Type de code QR détecté:", qrcode.type)
                        # Mise en commentaire de l'affichage de la zone de détection pour améliorer le temps d'exécution
                        # Extraire les coordonnées des coins du code QR
                        # (x, y, w, h) = qrcode.rect
                        # Jouer le son du bip lorsque le code QR est détecté
                        # son_bip.play()
                        #  Dessiner un rectangle autour du QrCode
                        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        #  Afficher la vidéo en temps réel avec les rectangles des codes QR
                        # cv2.imshow("Device_MALVEILLANTE_RECEPTRICE_Lecture_des_QRCodes_AFFICHES", frame)
                        #  Positionnement délai (milliSec)
                        # cv2.waitKey(10)
                        #  Déplacer la fenêtre à un emplacement spécifique de l'écran
                        # cv2.moveWindow("Device_MALVEILLANTE_RECEPTRICE_Lecture_des_QRCodes_AFFICHES", 0, 1500)  # Coordonnées x=100, y=100
                        #  Positionnement délai (milliSec)
                        # cv2.waitKey(10)
                        # recuperation du numéro de sequence dans qr_meta_data
                        # pour fabrication et affichage µqr_code
                        qrcode_data = qrcode.data.decode("utf-8")
                        qr_meta_data, data = qrcode_data.split(PATTERN_SEP, 1)
                        num_seq_qr, num_seq_max = qr_meta_data.split('/', 1)
                        # Affichage des données et des métadonnées
                        print("Métadonnées :", qr_meta_data)
                        make_qr_ack_pres(qr_meta_data)
                        # Sauvegarde des qrcodes détectés dans la liste list_qrcodes
                        list_qrcodes.append(qrcode)
                        if num_seq_qr == num_seq_max:
                            print("LastQRCodeAcquitté")
                            return
        except Exception as e:
            logging.exception("Une erreur s'est produite lors de la détection des QR codes : ", e)


if __name__ == '__main__':
    try:
        start_time = time.time()
        #  Test/préparation Environnement de travail
        for rep in (FOLDER_LOG, FOLDER_OUT):
            is_folder_exist(rep)
        list_qrcodes = []
        list_dec_datas = []
        # Initialiser la capture vidéo à partir de la webcam (0 --> webcam intégrée, 2 ou 4 pour webcams usb)
        capture = cv2.VideoCapture(0)
        detector_qr_aff()
        # Décoder le contenu du code QR en sortie de boucle
        for qrcode in list_qrcodes:
            qrcode_payload = qrcode.data.decode("utf-8")
            qrcode_type = qrcode.type
            metadata, qr_data45 = qrcode_payload.split(PATTERN_SEP, 1)
            # Afficher le contenu du code QR
            if qrcode_type == "QRCODE":  # sécurité contre les autres types que QRCODE (BARCODE)
                if qr_data45 not in list_dec_datas:
                    list_dec_datas.append(qr_data45)
        #  print (list_dec_datas)
        print(len(list_dec_datas))
        #  Enregistrer les données dans un fichier
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
        # Débit constaté le 26/05 : 1.4 Mo en 300 secondes
        # Soit 1400 Ko en 300 s → 4.66 Ko/s 1260 octets
        # Débit constaté le 31/05 : 1.4 Mo en 180 secondes,
        # Soit 1400 Ko en 180 s → 7.77 Ko/s 2300 octets
        # 10/07 1100 K0 en 180 secondes soit 6.25 Ko/s
    except Exception as e:
        logging.exception("Une erreur s'est produite lors de l'exécution du programme : ", e)

