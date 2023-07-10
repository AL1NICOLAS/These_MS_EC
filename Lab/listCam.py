import cv2

def lister_cameras_disponibles():
    index_cam = 2
    cameras_disponibles = []

    while True:
        # Essayez d'ouvrir la caméra avec l'index actuel
        cap = cv2.VideoCapture(index_cam)
        if not cap.isOpened():
            # Si l'ouverture échoue, cela signifie que la caméra n'est pas disponible
            break

        # Fermez la caméra pour libérer les ressources
        cap.release()
        # Ajoutez l'index de la caméra à la liste des caméras disponibles
        cameras_disponibles.append(index_cam)

        index_cam += 1

    return cameras_disponibles

# Utilisez la fonction pour lister les caméras disponibles
cameras_disponibles = lister_cameras_disponibles()

# Affichez les index des caméras disponibles
print("Caméras disponibles : ", cameras_disponibles)
