# =======================
#  Author : Alain NICOLAS
# =======================
# Ce programme lit et affiche une série de QRCodes (au format .png) présent dans un répertoire.
# Le balayage de la collection de QRCodes se fait par ordre alpha croissant
#   - il est déclenché par la captation (lecture et décodage) d'un QRCode"ACK" généré et affiché
#     par le programme décodeur sur le device attaquante

import time
import cv2
from natsort import natsorted
from pyzbar import pyzbar
import pygame
import logging
import os
from dotenv import load_dotenv
load_dotenv()
PATTERN_SEP = os.getenv("PATTERN_SEP")

# Initialiser pygame
pygame.mixer.init()
# Charger le son du bip
son_bip = pygame.mixer.Sound("./laserbip.wav")

PATH_ROOT = "../."   # "/home/lanig/PycharmProjects/These_MS_EC"
FOLDER_QR = f"{PATH_ROOT}/out_QRCodes"
FOLDER_LOG = f"{PATH_ROOT}/logs"
FILE_LOG = "/qrAfficheurWithQRAck_errors.log"
# Configurer le journal des erreurs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=FOLDER_LOG + FILE_LOG, level=logging.ERROR)

# Récupérer le nom du programme Python en cours d'exécution
nom_programme = os.path.basename(__file__)
print(f"\n\033[1m\033[4mNom du programme: \033[32m {nom_programme}\033[0m \n")


def reader_qr_seq_aff(image_file):
    try:
        # Convertir l'image en échelle de gris
        grayscale = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
        # Détecter les codes-barres dans l'image
        barcodes = pyzbar.decode(grayscale)
        # Parcourir les codes-barres détectés
        for barcode in barcodes:
            # Extraire le type de code-barre et les données
            data_qr_aff = barcode.data.decode('utf-8')
            # Afficher les résultats
            if barcode.type == "QRCODE":  # sécurité contre les autres types que QRCODE (BARCODE)
                print("Type code QR_ACQ lu:", barcode.type)
                metadata_text, data = data_qr_aff.split(PATTERN_SEP, 1)
                # Affichage des données et des métadonnées
                # print("Données du QR code :", data)
                print("Métadonnées :", metadata_text)
                return metadata_text
    except Exception as e:
        print("Erreur lors de la détection du QR code seq affichage : ", e)


def detector_qr_ack():
    try:
        list_qrcodes = ()
        # barcode = None  # Initialize the barcode variable
        while True:
            # Lire une image depuis la webcam
            ret, frame = capture.read()
            # Convertir l'image en échelle de gris
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Détecter les codes QR dans l'image
            barcodes_pyz = pyzbar.decode(gray)
            # print(len(barcodes_pyz))
            # Parcourir les codes QR détectés
            if len(barcodes_pyz):
                print(len(barcodes_pyz))
                i = 0
                barcode = ''
                for i, barcode in enumerate(barcodes_pyz):
                    # récupération de la seq lue
                    if barcode.type == "QRCODE":  # sécurité contre les autres types que QRCODE (BARCODE)
                        print("Type de code QR détecté ACK:", barcode.type)
                        # Extraire les coordonnées des coins du code QR
                        # (x, y, w, h) = barcode.rect
                        # Jouer le son du bip lorsque le code QR est détecté
                        # son_bip.play()
                        # Sauvegarde des qrcodes détectés dans la liste list_qrcodes
                        # list_qrcodes = list_qrcodes + (barcode,)
                        #  Dessiner un rectangle autour du QrCode
                        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        #  Afficher la vidéo en temps réel avec les rectangles des codes QR
                        # cv2.imshow("Device_BNPP_Lecture_des_QRCodes_ACK", frame)
                        #  Positionnement délai (milliSec)
                        # cv2.waitKey(5)
                        #  Déplacer la fenêtre à un emplacement spécifique de l'écran
                        # cv2.moveWindow("Device_CORPORATE_SOURCE_Lecture_des_QRCodes_ACK", 0, 0)  # Coordonnées x=100, y=100
                        #  Positionnement délai (milliSec)
                        # cv2.waitKey(5)
                        return barcode.data.decode("utf-8")
                break
            # Quitter la boucle si la touche 'q' est pressée
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print("Erreur lors de la détection du QR code ACK : ", e)


if __name__ == '__main__':
    try:
        start_time = time.time()  # Positionnement date heure début run
        # Chemin du dossier contenant les images QR codes
        image_folder = FOLDER_QR
        # Liste des noms des fichiers QR code dans l'ordre souhaité (tri avec natsort)
        list_qr_files = (file for file in os.listdir(image_folder))
        list_qr_files = natsorted(list_qr_files)

        # Initialiser la capture vidéo à partir de la webcam (0 --> webcam intégrée, 2 ou 4 pour webcams usb)
        capture = cv2.VideoCapture(6)
        # Parcourir les noms des fichiers QR code
        index = 0
        for index, qr_file in enumerate(list_qr_files):
            qr_code_path = os.path.join(image_folder, qr_file)
            print("Affichage du QR code seq : ", index + 1, f"==> {qr_code_path}")
            # Charger le fichier QR code
            qr_code = cv2.imread(qr_code_path)
            num_seq_aff = reader_qr_seq_aff(qr_code)
            # Attendre un court instant avant de passer au QR code suivant
            # Affichage du QRCode pour capture
            cv2.imshow("Device_CORPORATE_SOURCE_Affichage_QR_code_datas_out", qr_code)
            # Positionnement délai (milliSec)
            cv2.waitKey(2)
            # Déplacer la fenêtre à un emplacement spécifique de l'écran
            cv2.moveWindow("Device_CORPORATE_SOURCE_Affichage_QR_code_datas_out", 0, 200)  # Coordonnées x=100, y=100
            # Positionnement délai (milliSec)
            cv2.waitKey(100)
            while True:
                num_seq_ack = " "
                num_seq_ack = detector_qr_ack()
                print(f"num_seq_ack {num_seq_ack}  num_aff_seq {num_seq_aff}")
                if num_seq_ack == num_seq_aff:
                    print("Next")
                    break
        print(f"Fin de l'affichage des {index+1} QRCodes")
        cv2.waitKey(1)  # Temporisation dernière capture
        # Libérer la ressource de la capture vidéo
        capture.release()
        cv2.destroyAllWindows()  # Libérer les ressources
        # Affichage Fin de traitement
        print(f"\nFin du traitement d'affichage des {num_seq_ack} QRcodes ")
        end_time = time.time()
        duration = round((end_time - start_time), 3)
        print(f"\nDurée de traitement : \033[93m {duration}\033[0m seconde(s)")
    except Exception as e:
        print("Une erreur s'est produite lors de l'exécution du programme principal : ", e)
