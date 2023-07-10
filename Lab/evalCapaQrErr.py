import segno

# Liste des niveaux de correction d'erreur disponibles
error_correction_levels = ['L', 'M', 'Q', 'H']

# Taille maximale des données en fonction du niveau de correction d'erreur
data_sizes = []

# Taille maximale des données pour chaque niveau de correction d'erreur
for level in error_correction_levels:
    qr = segno.make('Example Data', error=level)
    data_sizes.append(qr.data_capacity)

# Affichage des résultats
for level, size in zip(error_correction_levels, data_sizes):
    print(f"Niveau de correction d'erreur {level}: {size} caractères")