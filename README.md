# Devoir 1

Ce dépôt contient l'énoncé et les fichiers nécessaires à la réalisation du
devoir 1 du cours INF5071 Infographie, de l'Université du Québec à Montréal,
enseigné à l'hiver 2018.

Le devoir doit être réalisé **seul**. Il doit être remis au plus tard le **16
mars 2018**, à 23h59. À partir de minuit, une pénalité de **2%** par heure de
retard sera appliquée.

## Remise du devoir

Afin de simplifier la remise, le devoir doit être remis par l'intermédiaire de
la plateforme GitLab. Pour ce faire, il suffit de cloner l'énoncé du devoir (ce
dépôt), de le rendre **privé**, puis de donner accès à l'utilisateur `ablondin`
(moi-même) en mode *Developer*. Les fichiers contenant les solutions aux
questions doivent se nommer `q1.py`, `q2.py`, `q3.py` et `q4.py`. Vous pouvez
utilisez Python 2.7 ou Python 3.x, mais je vous demanderais d'indiquer laquelle
des deux versions vous avez utilisée lors de la remise.

Remplissez le gabarit [solution.md](solution.md) en complément aux fichiers
Python fournis pour répondre aux différentes questions.

## Question 1

Dans cette question, vous devez fournir l'implémentation des classes `Point3D`
et `Vector3D` du module [geometry3d.py](files/geometry3d.py)

Les fonctions à implémenter sont identifiées par l'expression
```python
raise NotImplemented
```

Le comportement attendu pour chaque fonction est décrit dans la documentation
de la fonction, incluant des exemples. Notez qu'il est possible de vérifier de
façon automatique si les exemples fonctionnent bien à l'aide de la bibliothèque
[Doctest](https://docs.python.org/2/library/doctest.html) de Python. Plus
précisément, lorsque vous aurez terminé de répondre à cette question, on
s'attend à ce qu'à la commande
```sh
python -m doctest q1.py
```
lance une suite de tests automatiques qui réussiront tous.

## Question 2

L'objectif de cette question est de développer un petit programme Python qui
permet de modéliser une scène 2D simplifiée, dans laquelle évolue un rayon
lumineux.

### Sous-question 2.1

Dans un premier temps, vous devez implémenter le chargement de la scène. Une
scène est une boîte rectangulaire, de dimensions $`w \times h`$. Ses quatre
coins se trouvent donc en position $`(0,0)`$, $`(w,0)`$, $`(0,h)`$ et
$`(w,h)`$.

La scène peut contenir différents objets. Pour simplifier, nous supposerons que
les seuls types d'objets qui apparaissent dans une scène sont:

- des *cercles*, paramétrés par leur *centre* et leur *rayon* ou
- des *boîtes*, paramétrées par leur *centre*, leur largeur et hauteur.

Une scène sera représentée par un fichier au format JSON, tel qu'illustré par
le fichier [scene.json](exemples/scene.json) disponible dans ce dépôt. Notez
qu'il est très facile de manipuler un fichier au format JSON en Python,
puisqu'il existe un [module fourni par défaut directement dans la bibliothèque
standard](https://docs.python.org/2/library/json.html). Pour ne pas perdre trop
de temps, vous n'avez pas besoin de vérifier si le format du fichier est valide
ou non: vous pouvez prendre pour acquis que je testerai votre programme
seulement avec des scènes valides.

On s'attend donc à ce que la commande
```python
python q2.py exemple/scene.json
```
charge en mémoire la scène et affiche son contenu sur `stdout` quelque chose du
genre (vous avez une certaine liberté au niveau de l'affichage):
```python
Scene of dimensions 400 x 300
Containing 3 objects:
- A circle of radius 50, centered in (200,300)
- A circle of radius 100, centered in (400,0)
- A box of width 100 and height 30, centered in (100,100)
```

### Sous-question 2.2

Lorsque vous aurez implémenté le chargement de la scène, vous devrez ensuite
offrir un service qui permet de générer la scène dans une image au format PNG,
à l'aide de la bibliothèque [Pillow](https://pillow.readthedocs.io/en/latest/).
Dans cette scène, il suffira simplement d'afficher les cercles et les boîtes au
bon endroit, ainsi que les limites.

Ainsi, on aimerait que la commande
```python
python q2.py exemple/scene.json scene.png
```
produise un fichier `scene.png` représentant la scène décrite dans le fichier
`exemple/scene.json`.

### Sous-question 2.3

Finalement, vous devrez tracer la propagation d'un rayon lumineux à l'intérieur
de votre scène. Un rayon lumineux est décrit par les paramètres suivants:

- Son *point de départ*, représenté par un point 2D;
- Sa *direction*, représentée par un vecteur 2D;
- Son *intensité*, représentée par un entier positif.

Lorsqu'un rayon lumineux percute un objet de la scène ou une des limites de la
scène, il est réfléchi selon le vecteur normal à la surface ou se fait le
contact. Comme les objets sont des boîtes ou des cercles, il est relativement
facile de calculer leur vecteur normal en tout point de contact.

Finalement, vous devrez tenir compte de l'intensité de la lumière pour évaluer
le nombre de *rebonds* qui peuvent être effectués par le rayon lumineux. Plus
précisément, le rayon fera un nombre de bond égal à son intensité. Par exemple,
si son intensité est $`5`$, alors il sera réfléchi $`5`$ fois.

On s'attend donc à ce que la commande
```python
python q2.py exemple/scene.json scene.png 20,20,5,3,8
```
produise un fichier `scene.png` représentant la scène décrite dans le fichier
`exemple/scene.json` avec un rayon (identifié par une couleur différente des
objets pour mieux le repérer) qui démarre au point $`(20,20)`$, en direction
$`(5,3)`$ et qui effectue $`8`$ rebonds.

Ici aussi, vous pouvez supposer que le rayon lumineux aura un point de départ
valide, c'est-à-dire qu'il se situera toujours dans la scène, et qu'il ne sera
pas à l'intérieur d'un des objets.

## Question 3

Nous avons vu en classe qu'une sphère de rayon $`r`$ centrée en $`(0,0)`$
pouvait être paramétrisée par la fonction vectorielle
```math
s(u,v) = (r\sin(u)\cos(v), r\sin(u)\sin(v), r\cos(u))
```

Écrivez un programme en Python, nommé `q3.py` qui permet de générer une
sphère au format OBJ. Les trois paramètres considérés sont

- $`r`$: le rayon de la sphère;
- $`u_n`$: le nombre de "méridiens";
- $`v_n`$: le nombre de "parallèles".

Plus précisément, on s'attend à ce que la commande
```sh
python q3.py sphere 5 32 16 > sphere.obj
```
produise le fichier [sphere.obj](exemples/sphere.obj) disponible dans ce dépôt.

Notez que vous n'avez pas à indiquer les coordonnées de texture dans le
fichier, mais vous devez préciser les vecteurs normaux.

Ensuite, étendez votre programme `q3.py` pour qu'il génère un tore. L'équation
paramétrique du tore est assez similaire à celle de la sphère:
```math
s(u,v) = ((R + r\cos(v))\cos(u), (R + r\cos(v))\sin(u), r\sin(v))
```

Vous utiliserez donc les paramètres suivants:

- $`R`$: le rayon majeur du tore (c'est-à-dire la distance entre le centre du
  tore et le centre du *tube* qui constitue le tore;
- $`r`$: le rayon mineur du tore (c'est-à-dire le rayon du tube);
- $`u_n`$: le nombre de "méridiens" dans le tore;
- $`v_n`$: le nombre de "parallèles".

Ainsi, on s'attend à ce que la commande
```sh
python q3.py tore 5 2 32 16 > tore.obj
```
produise un tore avec les paramètres $`R = 5`$, $`r = 2`$, $`u_n = 32`$ et
$`v_n = 16`$.

## Question 4

En vous inspirant du tutoriel YouTube disponible au lien
[https://www.youtube.com/watch?v=nmLjYSmaW48](https://www.youtube.com/watch?v=nmLjYSmaW48),
écrivez un script Blender qui permet de générer une animation simplifiée d'un
système solaire. Votre script devra prendre en entrée un fichier au format JSON
qui indiquera la valeur des paramètres. Un exemple se trouve dans le fichier
[solar-system.json](exemples/solar-system.json)

Quelques explications sur les paramètres:

- `"name"` est le nom de l'étoile ou de la planète. Il n'est pas vraiment utile
  pour l'animation, mais permet d'identifier les objets.
- `"radius"` est le rayon de la sphère qui représente l'étoile ou la planète.
- `"color"` est un triplet RGB qui représente la couleur (*diffuse*) du
  matériau utilisé pour représent l'objet. Vous êtes libre d'ajouter une
  réflexion spéculaire ou une texture supplémentaire pour donner un relief à
  vos objets.
- `"distance-from-star"` est la distance (en unité Blender) du centre de
  l'objet par rapport au centre de l'étoile.
- `"period"` est le nombre d'images (*frames*) qu'il faut compléter pour qu'une
  planète fasse un tour complet autour de l'étoile.

Comme il s'agit d'un cours d'infographie, vous n'avez pas besoin de valider si
le fichier JSON est intègre: vous pouvez supposer que votre animation sera
testée avec des données valides. Assurez-vous cependant que la caméra capture
bien la totalité des orbites de chaque planète. Il est également recommandé de
ne pas démarrer à partir d'un script vide. Par exemple, le script
[generate_scene.py](https://gitlab.com/ablondin/inf5071-exercices/blob/master/exemples/generate_scene.py)
constitue un bon point de départ.

Au niveau du comportement, on s'attend à ce que la commande
```sh
python q4.py exemples/solar-system.json initial.blend animation.ogg
```
produise une animation au format OGG (c'est un format relativement portable
supporté directement dans Blender), en prenant les informations dans le fichier
`exemples/solar-system.json` et utilisant un fichier `initial.blend` dans
lequel des objets prédéfinis existent déjà. Notez que l'utilisation du fichier
`initial.blend` est optionnelle, mais elle peut simplifier une partie de la
configuration de certains aspects de l'animation, par exemple la position de la
caméra, l'arrière-plan de l'image produite, etc.
