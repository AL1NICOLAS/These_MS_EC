# Projet These_MS_EC ==> POC Exfiltration de données via le vecteur QRCodes en environnement air-gap.
Auteur : Alain NICOLAS.

Cet ensemble de **3** programmes python constitue la solution permettant de démontrer qu'il est possible d'exfiltrer
des données de toutes natures depuis une device source vers une device réceptrice sans utiliser la connectivité réseau.
Ce POC utilise la technologie des QRCodes comme vecteur de données.

Voici la description de chacun des 3 programmes et des modalités de leur utilisation :

    Programme 1 ==> qrEncoder_OnDeviceEmission_WithSeq.py


1. [ ] Exécution de ce programme sur la **device CORPORATE source** des datas à exfiltrer.

Ce programme encode des datas à exfiltrer sous forme d'une collection de QRCodes.
Le collaborateur malveillant rassemble l'ensemble des documents dans le répertoire `"./../in_files_to_exfiltrate"`
Après avoir constitué une archive qui ensuite est compressée "payload.tar.gz", le binaire
du zip est encodé en base45. Le payload base45 est découpé en partie de 4270 caractères afin de générer
autant de QRCodes que nécessaire. 
Chaque QRCode généré est flanqué en début de data de l'information du numéro de la séquence / le nombre total
de QrCodes produits.

Ex : **1/6** suivi d'un séparateur **%%::%%** suivies des données base45

    Programme 2 ==> qrAfficher_OnDeviceEmission_WithQrAck.py


1. [ ] Exécution de ce programme sur la **device CORPORATE source** des datas à exfiltrer.

Ce programme lit et affiche la série de QRCodes .png produits par le **Programme 1**.
Le balayage de la collection de QRCodes 
* se fait par ordre alphanumérique croissant sur le nom du.png suffixé 
du numéro de séquence 
* est déclenché par la captation (lecture et décodage) d'un QRCode "ACK" généré et affiché
par le **Programme 3** décodeur sur la device malveillante destinatrice des données.
  * L'index de la webcam de la device CORPORATE est à positionner dans cv2.VideoCapture( ? )
  * le QRCode ACK contient simplement le rang de la séquence et le nombre total de séquence : 
    * Ex : **1/6**

Ainsi le Programme 2 et le Programme 3 se synchronise jusqu'à l'affichage et la captation 
du dernier qrcode du run d'exfiltration sans rupture de séquence.

    Programme 3 ==> qrDecoder_OnDeviceReception_WithQrAck.py

1. [ ] Exécution de ce programme sur la **device MALVEILLANTE destinatrice** des datas à exfiltrer.

Ce programme est lancé en même temps que **le Programme 2 Afficheur** permet de lire et décoder les QrCodes 
affichés par la device CORPORATE Source et contenant les données à exfiltrer.
L'index de la webcam de la device MALVEILLANTE réceptrice est à positionner dans cv2.VideoCapture( ? )
Lorsque que l'un des QRCodes est lu et décodé, la data en est extraite et mise en liste puis
un QRCode d'acquittement contenant en data la séquence acquittée est généré et affiché
dans le but d'être scanné, analysé et décodé par le Programme 2 Afficheur sur la device source 
qui se synchronise et affiche le QRcode suivant.
Lorsque tous les QRCodes sont reçus, le Programme 2 se termine, les datas sont concaténées et décodées de la base45 pour
restituer le payload binaire tar.gz.
La sortie de Programme 3 affiche l'emplacement sur le disque.

ex : 
_Fin du traitement de décodage et ré-assemblage.
==> Emplacement de l'archive tar.gz sur le disque :_ 
"[file:///home/user/PycharmProjects/These_MS_EC/decodedOut/datasLeakOut.tar.gz]()"

    Diagramme de séquence :
![exfiltrationDataPOCPres.png](Documentation%2FexfiltrationDataPOCPres.png)