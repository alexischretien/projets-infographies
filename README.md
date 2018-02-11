# Devoir 1

Ce dépôt contient l'énoncé et les fichiers nécessaires à la réalisation du
devoir 1 du cours INF5071 Infographie, de l'Université du Québec à Montréal,
enseigné à l'hiver 2018.

Ce devoir doit être réalisé **seul**.

## Remise du devoir

Afin de simplifier la remise, le devoir doit être remis par l'intermédiaire de
la plateforme GitLab. Pour ce faire, il suffit de cloner l'énoncé du devoir (ce
dépôt), de le rendre **privé**, puis de donner accès à l'utilisateur `ablondin`
(moi-même) en mode *Developer*. Les solutions aux questions devront se trouver
dans des dossiers `question`

## Question 1

À compléter.

## Question 2

À compléter.

## Question 3

Nous avons vu en classe qu'une sphère de rayon $`r`$ centrée en $`(0,0)`$
pouvait être paramétrisée par la fonction vectorielle
```math
s(u,v) = (r\sin(u)\cos(v), r\sin(u)\sin(v), r\cos(v))
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

À compléter.
