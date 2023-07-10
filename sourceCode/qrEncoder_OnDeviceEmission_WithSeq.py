# =======================
#  Author : Alain NICOLAS
# =======================
#  Ce programme encode des datas à exfiltrer sous forme d'une collection de QRCodes.
#  Après avoir constitué une archive qui ensuite est compressée, le binaire
#  du zip est encodé en base64. L'information base64 est découpée afin de générer
#  autant de QRCodes que nécessaires :
import base45
import shutil
import tarfile
import time
import segno
import logging
import os
from dotenv import load_dotenv
load_dotenv()
PATTERN_SEP = os.getenv("PATTERN_SEP")
# CONSTANTES environnement
PATH_ROOT = "../."   # "/home/lanig/PycharmProjects/These_MS_EC"
FOLDER_IN = f"{PATH_ROOT}/in_files_to_exfiltrate"
FOLDER_QR = f"{PATH_ROOT}/out_QRCodes"
FOLDER_LOG = f"{PATH_ROOT}/logs"
FOLDER_TMP = f"{PATH_ROOT}/temp"
OUTPUT_TAR_FILENAME = f"{PATH_ROOT}/temp/exFiles.tar.gz"
FILE_LOG = "/qrEncoder_errors.log"
# Récupérer le nom du programme Python en cours d'exécution
nom_programme = os.path.basename(__file__)
print(f"\n\033[1m\033[4mNom du programme: \033[32m {nom_programme}\033[0m \n")

# variables paramétriques
part_size = 4270  # Découpage : taille de datas/ QRcode (en octets) / 2953 max base64, 4296 base45

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
            #  Recréer le répertoire vide
            os.mkdir(path)
        else:
            #  Recréer le répertoire vide
            os.mkdir(path)
    except Exception as err2:
        logging.error(f"Erreur lors de la suppression du répertoire : {err2}")


if __name__ == '__main__':
    start_time = time.time()
    try:
        #  Test/préparation Environnement de travail
        for rep in (FOLDER_LOG, FOLDER_IN, FOLDER_QR, FOLDER_TMP):
            is_folder_exist(rep)
        # Configurer le journal des erreurs
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=FOLDER_LOG + FILE_LOG, level=logging.ERROR)
        #  Utilisation de la fonction vider_repertoire pour initialiser l'environnement
        vider_repertoire(FOLDER_QR)
        #  Tar&zip des données à exfiltrer
        create_tar(FOLDER_IN, OUTPUT_TAR_FILENAME)

        with open(OUTPUT_TAR_FILENAME, "rb") as f:
            #  Découpage du contenu du fichier à exfiltrer en plusieurs parties de taille fixe
            #  Taille de découpage de la data encodée b64 (en caractères) contenue dans chaque QRCode
            #  Directement liée à la qualité de la correction d'erreur choisie (segno.make_qr)
            fileContent = f.read()
            #  Convertir les données du fichier ZIP en base64
            fileContentBase45 = base45.b45encode(fileContent).decode("utf-8")
            #  Découpage pour constituer les codes QR
            list_parts = [fileContentBase45[i: i + part_size] for i in range(0, len(fileContentBase45), part_size)]

        #  Génération des codes QR pour chaque partie
        qr_codes = []
        max_seq = len(list_parts)
        print(f"max_seq ==> {max_seq}")
        index = 0
        for index, datas_b45 in enumerate(list_parts):
            datas_b45_ind = ''
            datas_b45_ind = f'{index+1}/{max_seq}{PATTERN_SEP}{datas_b45}'
            qr_codes.append(segno.make_qr(datas_b45_ind, mode="alphanumeric"))
        #  Enregistrement des codes QR sous forme d'images PNG
        ind = 0
        for ind, qr_code in enumerate(qr_codes):
            qr_code.save(f"{FOLDER_QR}/qr_code_part{ind}.png",
                         # dark='#1B5E20',
                         # dark='black',
                         # light='white',
                         # data_dark='#1B5E20',
                         # data_light='',
                         # border=2,
                         scale=3)
        print(f"\nFin du traitement d'encodage ==> \033[92m{ ind + 1 }\033[0m QRCodes générés")
        end_time = time.time()
        duration = round((end_time - start_time), 3)
        print(f"\nDurée de traitement : \033[93m {duration}\033[0m seconde(s)")
    except Exception as err3:
        logging.error(f"Une erreur s'est produite dans le traitement main : {err3}")
