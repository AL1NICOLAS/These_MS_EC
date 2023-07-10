# =======================
# Author : Alain NICOLAS
# =======================
# Ce programme lit et affiche une série de QRcodes (au format .png) présent dans un répertoire.
# Le balayage de la série de QRcodes se fait par ordre alpha croissant
#   - il est déclenché par la captation d'un son normalisé et ayant un taux de corrélation
#     calculé et corrélé à un son référence afin d'éviter les sons parasites.
# TO_DO Refaire test débit avec Nouvelle temporisation de 15 ms var_duration
import time
import cv2
import os
from natsort import natsorted
import sounddevice as sd
import numpy as np
import pygame as pg
import soundfile as sf
import logging

# CONSTANTES environnement
PATH_ROOT = "./.."   # "/home/lanig/PycharmProjects/ThèseProUttMS_EFC"
FOLDER_QR = f"{PATH_ROOT}/out_QRCodes"
FOLDER_LOG = f"{PATH_ROOT}/logs"
FOLDER_TMP = f"{PATH_ROOT}/temp"
FILE_LOG = "/qrAfficheurWithSound_errors.log"

# variables paramétriques
duration = 0.15  # Durée d'enregistrement en secondes (0.150 le 26/05)
sample_rate = 44100  # Taux d'échantillonnage
channels = 1  # Nombre de canaux (mono)

# Chargement des fichiers audio
path_soundLaser = "./laserbip.wav"       # Son de référence

# Configurer le journal des erreurs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename=FOLDER_LOG + FILE_LOG,
                    level=logging.INFO)

# Récupérer le nom du programme Python en cours d'exécution
nom_programme = os.path.basename(__file__)
print(f"\n\033[1m\033[4mNom du programme: \033[32m {nom_programme}\033[0m \n")


if __name__ == '__main__':
    try:
        start_time = time.time()  # Positionnement date heure début run
        sound_laser, sample_rate = sf.read(path_soundLaser)  # Chargement du son de référence

        # Initialisation de pygame pour le bip
        pg.mixer.init()
        print("Attente de la détection du son ...")

        # Liste des noms des fichiers QR code dans l'ordre souhaité (tri avec natsort)
        qr_files = []
        qr_files = os.listdir(FOLDER_QR)
        qr_files = natsorted(qr_files)

        # Parcourir les noms des fichiers QR code
        for qr_file in qr_files:
            print("Affichage du QR code:", f"{FOLDER_QR}/{qr_file}")
            # Charger le fichier QR code
            qr_code = cv2.imread(f"{FOLDER_QR}/{qr_file}")
            # Attendre un court instant avant de passer au QR code suivant
            while True:
                # Affichage du QRCode pour capture
                cv2.imshow("Afficheur_QR_code", qr_code)
                # Positionnement délai
                cv2.waitKey(5)
                # Déplacer la fenêtre à un emplacement spécifique de l'écran
                cv2.moveWindow("Afficheur_QR_code", 100, 600)  # Coordonnées x=100, y=100
                cv2.waitKey(100)
                # time.sleep(0.2) # 0.2 # Temporisation possible du débit d'affichage
                recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
                sd.wait()  # Attente de la fin de l'enregistrement
                max_correlation = 0
                if np.max(recording) > 0.1:  # Ajustez le seuil de détection selon vos besoins
                    print(f"{np.max(recording)} Son détecté !")
                    # detection son laser
                    # Conversion en tableaux NumPy 1D avant Normalisation de la capture
                    sound_laser = sound_laser.flatten()
                    sound_laser_normalized = sound_laser / np.max(np.abs(sound_laser))
                    recording = recording.flatten()
                    recording_normalized = recording / np.max(np.abs(recording))
                    # Comparaison des signaux audio (signal capté avec signal référence) avec la corrélation croisée
                    correlation = np.correlate(sound_laser_normalized, recording_normalized, mode='full')
                    # correlation = np.correlate(sound_laser, recording, mode='full')
                    max_correlation = np.max(correlation)
                    print("Corrélation maximale :", max_correlation)
                    if max_correlation >= 180:  # affichage qrcode suivant si seuil de correlation atteint
                        print("Next")
                        break
                else:
                    print("Aucun son détecté.")
        print("fin de l'affichage")
        cv2.waitKey(10)  # Temporisation dernière capture
        cv2.destroyAllWindows()  # Libérer les ressources
        # Affichage Fin de traitement
        print(f"\nFin du traitement d'affichage des QRcodes ")
        end_time = time.time()
        duration = round((end_time - start_time), 3)
        print(f"\nDurée de traitement : \033[93m {duration}\033[0m seconde(s)")
    except Exception as e:
        logging.exception("Une erreur s'est produite lors de l'exécution du programme : ", e)
