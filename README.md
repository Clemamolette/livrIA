# livrIA

<img src="src/logo livria.png" width="500em">

LivrIA est une solution d'IA permettant d'obtenir la liste des livres présent dans une phot de biliothèque.

La liste d'application est multiple, ce workflow peut s'inscrire dans un projet de gestion d'inventaire pour les bibliothèques, de suivi de collection personnelle ou de recherche d'un livre précis sur une étagère de livres non triés.

### Prérequis
Nous utilisons des modèles de vision pour lire les caractères sur la tranche du livre. Il est donc nécessaire d'avoir les modèles suivant avec ollama : 
- minicpm-v
- llava-phi3
- llama3.2-vision

Pour les installer, utiliser ollama :
```
ollama pull nom_modele
```


### Installation

Pour installer les requirements python, à la racine du projet :
```
pip install -r erquirements.txt
```

Pour lancer l'application, à la racine du projet :
```
./run.sh
```


### Configuration machine CY
Platform system: Linux-5.15.0-127-generic-x86_64-with-glibc2.31
Python version: 3.12.5
CodeCarbon version: 2.8.3
Available RAM : 15.305 GB
CPU count: 8
CPU model: 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
GPU count: None
GPU model: None

Pendant une utisation bureautique du PC :
Energy consumed for RAM : 0.005628 kWh. RAM Power : 5.739555358886719 W
Energy consumed for all CPUs : 0.013728 kWh. Total CPU Power : 14.0 W
0.000307 g.CO2eq/s mean an estimation of 9.689878123439193 kg.CO2eq/year

