#1 Changement de la carte
Copier votre fichier "map.json" dans le répertoire racine du fichier "hicab_server.py"
Note: Veillez à conserver le nom "map.json"


#2 Connection réseau
Le RaspberryPi est configuré pour être un point d'accès wifi, ainsi que serveur DHCP
La connection au réseau est possible sur les deux interfaces:
	- Wifi: Connectez-vous au SSID "HiCab-Wifi" avec le passkey "hicabify"
	- Ethernet: Connectez un switch ou directement sur le port ethernet du Raspberry


#3 Démarrage du serveur HiCab
A l'aide d'un client SSH, connectez vous sur 192.168.1.1 (wifi) ou 192.168.2.1 (ethernet)
Entrez les commandes suivantes:
	cd /home/pi/hicab/
	sudo gunicorn -k flask_sockets.worker -b 0.0.0.0:80  hicab_server:app


#4 Urls accessibles
http://addresse_ip/ => IHM Display/Requester
http://addresse_ip/simulation?device_type=cab_device => Simulateur du device embarqué dans le taxi
http://addresse_ip/simulation?device_type=display_device => Simulateur de l'IHM Display/Requester


#5 Remerciements
Nous tenons à remercier:
	- Guilhem Bideau - IMERIR - Promotion Parcevaux, pour son soutien lors configuration du RaspBerryPi
	- Marc Danjoux - IMERIR - Promotion Parcevaux, pour ses conseils avisés en Mathématiques
	- L'inconnu qui a proposer son algorithme Dijsktra sur http://informathix.tuxfamily.org/?q=node/119
	- L'équipe enseignante pour leurs disponibilités et leurs conseils tout au long de ce projet