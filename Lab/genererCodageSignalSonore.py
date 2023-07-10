import numpy as np
import sounddevice as sd


def generate_coded_signal(sequence, bit_duration=0.1, sample_rate=44100, frequency_0=1000, frequency_1=2000):
    # Convertir la séquence en une séquence binaire
    binary_sequence = [int(bit) for bit in bin(sequence)[2:]]

    # Créer les échantillons pour chaque bit de la séquence
    t = np.linspace(0, bit_duration, int(bit_duration * sample_rate), endpoint=False)
    signal = np.concatenate([
        np.sin(2 * np.pi * frequency_0 * t) if bit == 0 else np.sin(2 * np.pi * frequency_1 * t)
        for bit in binary_sequence
    ])
    return signal

# Exemple : Générer le codage de la séquence 123 et émettre le son
sequence = 12
signal = generate_coded_signal(sequence)

sd.play(signal)
sd.wait()
