import cv2
import os
import numpy as np

# Chemin du dossier contenant les images
folder_path = "../encoded"

# Liste des noms de fichiers d'images dans le dossier
image_files = os.listdir(folder_path)

# Création de la fenêtre
window_name = "Images Grid"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Taille des images dans la grille
grid_size = (2,2 )

# Dimensions cibles pour redimensionner les images
target_width = 555
target_height = 555

# Liste pour stocker les images redimensionnées
resized_images = []

# Redimensionner les images tout en maintenant le ratio d'aspect
for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)
    image = cv2.imread(image_path)

    # Récupérer les dimensions de l'image
    height, width, _ = image.shape

    # Calculer le facteur de redimensionnement pour conserver le ratio d'aspect
    aspect_ratio = min(target_width / width, target_height / height)
    new_width = int(width * aspect_ratio)
    new_height = int(height * aspect_ratio)

    # Redimensionner l'image en utilisant les nouvelles dimensions
    resized_image = cv2.resize(image, (new_width, new_height))
    resized_images.append(resized_image)

# Créer une grille d'images
grid_img = np.zeros((target_height * grid_size[1], target_width * grid_size[0], 3), dtype=np.uint8)
row, col = 0, 0
image_count = 0

while image_count < len(resized_images):
    image = resized_images[image_count]

    # Ajouter l'image à la grille
    grid_img[row * target_height:(row + 1) * target_height, col * target_width:(col + 1) * target_width] = image

    col += 1
    if col >= grid_size[0]:
        col = 0
        row += 1

    image_count += 1

    if row >= grid_size[1]:
        # Toutes les cellules de la grille sont remplies, afficher la grille et attendre une touche pour continuer
        cv2.imshow(window_name, grid_img)
        key = cv2.waitKey(0)

        if key == ord('q'):
            break

        row, col = 0, 0
        grid_img = np.zeros((target_height * grid_size[1], target_width * grid_size[0], 3), dtype=np.uint8)

# Afficher la dernière grille si elle n'est pas complète
if grid_img.any():
    cv2.imshow(window_name, grid_img)
    cv2.waitKey(0)

cv2.destroyAllWindows()