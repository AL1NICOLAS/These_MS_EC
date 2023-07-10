import sounddevice as sd
import numpy as np

def decode_signal(signal, bit_duration=0.1, sample_rate=44100, frequency_0=1000, frequency_1=2000):
    # Déterminer le nombre d'échantillons par bit
    samples_per_bit = int(bit_duration * sample_rate)

    # Calculer la limite pour discriminer les fréquences
    threshold = (frequency_0 + frequency_1) / 2

    # Décoder les échantillons
    decoded_sequence = []
    for i in range(0, len(signal), samples_per_bit):
        bit_signal = signal[i:i+samples_per_bit]
        frequency = np.abs(np.fft.fft(bit_signal)[:len(bit_signal)//2])

        if np.mean(frequency) > threshold:
            decoded_sequence.append(1)
        else:
            decoded_sequence.append(0)

    # Convertir la séquence binaire en un nombre entier
    decoded_number = int(''.join(map(str, decoded_sequence)), 2)

    return decoded_number

# Exemple : Capturer le son et le décoder
duration = 10 # Durée d'enregistrement en secondes
sample_rate = 44100

recorded_signal = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()

decoded_number = decode_signal(recorded_signal[:, 0])

print("Numéro décodé :", decoded_number)
