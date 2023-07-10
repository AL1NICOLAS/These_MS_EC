from pydub import AudioSegment
from pydub.generators import Sine

# Fréquence du bip en Hz
frequency = 50000  # def 50000

# Durée du bip en millisecondes
duration = 10  # def 10

# Générer le bip
bip = Sine(frequency).to_audio_segment(duration=duration)

# Enregistrer le bip dans un fichier WAV
bip.export("laserbip.wav", format="wav")
