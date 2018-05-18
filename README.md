# Projets d'infographies

## Description 
Ce dépot contient trois programmes réalisés dans le cadre du cours INF5071 
de l'UQAM, donné par Alexandre Blondin Massé. 
## Auteur

Alexis Chrétien

## Scene

Le fichier [scene.py](scene.py) contient l'implémentation d'un programme générant une
scène composé de boites et de cercles. Le lancement du programme se fait via l'exécution 
d'une commande de la forme :
```
python scene.py FICHIER_SCENE [<OPTIONNEL> FICHIER_IMAGE [<OPTIONNEL> OX,OY,DX,DY,I ] ]
```
* `FICHIER_SCENE` : Le chemin relatif vers un fichier au format JSON contenant les 
                    informations sur une scene composée de cercles et de boites.
* `FICHIER_IMAGE` : Le nom de fichier de l'image à produire.
* `OX` :            La coordonnée en x du point d'origine du rayon de lumière.
* `OY` :            La coordonnée en y du point d'origine du rayon de lumière. 
* `DX` :            La coordonnée en x du vecteur de direction du rayon de lumière.
* `DY` :            La coordonnée en y du vecteur de direction du rayon de lumière.
* `I` :             L'intensité du rayon de lumière, correspondant au nombre de fois 
                    qu'il peut rebondir. 

Si seulement `FICHIER_SCENE` a été spécifié, le programme affiche les informations de la 
scène à la sortie standard. Si `FICHIER_IMAGE` a aussi été spécifié, une image représentant la 
scène est également produite. Enfin, si les paramètres du rayon de lumière sont aussi présents,
le tracé du chemin parcouru par ce rayon est également tracé dans la même image, en orange.  

Par exemple, la commande
```
python scene.py exemples/scene.json scene.png 20,20,5,3,8
```
permet d'affichier à la sortie standard le contenu de la scène décrite dans le le fichier 
`exemples/scene.json` et crée l'image `scene.png` représentant la scène ainsi que le tracé 
d'un rayon de lumière d'origine (20,20) de direction (5,3) et d'intensité 8.  

## Spheroide

Le fichier [spheroide.py](spheroide.py) contient l'implémentant d'un programme permettant 
d'afficher l'équivalent d'un fichier au format OBJ décrivant une sphère ou un tore. Le lanchement du 
programme se fait via l'exécution d'une commande de la forme
```
python spheroide.py [sphere [R] [U] [V] | tore [RMAJ] [RMIN] [U] [V] ]
```
* `R` :    Le rayon d'une sphère. 
* `RMAJ` : Le rayon majeur d'un tore.
* `RMIN` : Le rayon mineur d'un tore.
* `U` :    Le nombre de longitudes.
* `V` :    Le nombre de latitudes. 

par exemple, la commande
```
python spheroide.py tore 5 2 32 16
```
Permet d'afficher à la sortie standard le contenu d'un fichier OBJ décrivant un tore de rayon 
majeur 5, de rayon mineur 2 et ayant 32 longitudes et 16 latitudes.

Pour produire un fichier OBJ plutôt que d'afficher les informations, rediriger le contenu via un pipeline. 
Par exemple :
```
python spheroide.py tore 5 2 32 16 > tore.obj
```
## Système solaire

Le fichier [sys-blenderscript.py](sys-blenderscript.py) contient l'implémentation d'un scripte Blender.
Celui-ci doit donc nécessairement être exécuté dans l'environnement de Blender, se dont le script [sys.py](sys.py) 
se charge de faire. 

Le programme permet de générer le fichier vidéo de format OGG d'une animation de 10 secondes
sur l'évolution d'un système solaire décrit dans un fichier au format JSON. Le programme
est lancé via la commande
```
python sys.py [FICHIER_JSON] [FICHIER_ANIMATION]
``` 
* `FICHIER_JSON`     : Le chemin relatif du fichier JSON décrivant le système solaire.
* `FICHIER_ANIMATION`: Le nom du fichier OGG à produire.

Exemple d'utilisation : 
```
python sys.py exemples/solar-system.json animation.ogg
``` 

## Dépendances

* Python 2.7.12
* Blender 2.79
* Pillow 5.0.0 (librairie Python)

## Références

* [Diapositives du cours INF5071](http://lacim.uqam.ca/~blondin/fr/inf5071)
* [Stack Overflow](https://stackoverflow.com/questions/1549909/intersection-on-circle-of-vector-originating-inside-circle) : Pour trouver l'intersection entre une ligne droite et un cercle en utilisant une approche vectorielle. 
