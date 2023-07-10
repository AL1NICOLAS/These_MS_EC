import sounddevice as sd
import numpy as np
import pygame
import soundfile as sf
 
duration = 0.4 # Durée d'enregistrement en secondes 0.550
sample_rate = 22050 # Taux d'échantillonnage
channels = 1  # Nombre de canaux (mono)

# Chargement des fichiers audio
path_soundLaser = "../sourceCode/laser.wav"
path_soundRec = "capture.wav"
# Initialisation de pygame pour le bip
pygame.mixer.init()


print("Attente de la détection du son...")

while True:
    # Enregistrement audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    #print(recording)
    # Sauvegarde dans un fichier WAV
    sd.wait()  # Attente de la fin de l'enregistrement
    max_correlation = 0
    # Vérification si un son est détecté
    if np.max(recording) > 0.1:  # Ajustez le seuil de détection selon vos besoins**
        print(f"{np.max(recording)} Son détecté !")
        # detection son laser
        # Charger les fichiers audio
        # Charger les fichiers WAV
        sound_laser, sample_rate = sf.read(path_soundLaser)

        # Conversion en tableaux NumPy 1D
        sound_laser = sound_laser.flatten()
        sound_laser_normalized = sound_laser / np.max(np.abs(sound_laser))
        recording = recording.flatten()
        recording_normalized = recording / np.max(np.abs(recording))
        # Comparaison des signaux audio avec la corrélation croisée
        correlation = np.correlate(sound_laser, recording, mode='full')
        max_correlation = np.max(correlation)

        print("Corrélation maximale :", max_correlation)
    else:
        print("Aucun son détecté.")