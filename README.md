# projet-ia-jeux-2021
Template pour le projet L3 IA et Jeux, 2021, Sorbonne Univ.

## Présentation du projet

Dans un problème de *cooperative path-finding*: on dispose d'un ensemble d'agents qui doivent chacun atteindre une destination qui leur est propre. Il s'agit de trouver un ensemble de chemins, sans collision, qui permette à chaque agent d'atteindre sa destination.

Une approche coordonnée classique permettant d'aborder ce problème est l'algorithme *cooperative A** [1]: les agents cherchent de manière coopérative leur chemin dans un espace tri-dimensionnel (on ajoute le temps, de manière à gérer les conflits éventuels avec les chemins des autres joueurs). On note que les joueurs peuvent donc également faire une pause dans leur déplacement. (De nombreuses autres approches sont envisageables).


L'objet de ce projet est d'étudier une version *adversariale* du cooperative path-finding: plusieurs équipes d'agents sont en compétition et cherchent à atteindre leurs destinations *avant* leurs adversaires. On se limitera dans ce projet à deux équipes.
Afin d'éviter les situations de blocage, on fixera à l'avance une limite sur le nombre de tours du jeu.
On constate que au niveau global, on peut donc voir ce problème comme un jeu à 2 joueurs dans lequel chaque équipe est un meta-joueur. En effet, les actions au sein de chaque équipe peuvent éventuellement être coordonnées, comme c'est le cas dans l'algorithme de cooperative path-finding mentionné précédemment.  

Comme critère de victoire, on considère :
* l'équipe qui a réussi a placer le plus d'agents à leur destination, et en cas d'égalité,
* l'équipe dont la somme pour sur les agents de l'équipe des plus courts chemins à leur destination est la plus faible.

(Il est ainsi possible de déclarer une équipe victorieuse même si toutes les destinations ne sont pas atteintes).


Les déplacements des équipes obéissent à quelques règles précises:
* les tours alternent entre équipes: les agents de l'équipe A peuvent tous bouger, puis ceux de l'équipe B, etc.
* les agents se déplacent sur une case adjacente ou restent au même endroit;
* il faut éviter toute collision: un agent peut se déplacer vers une case si celle-ci est libre ou libérée dans le même tour par un joueur de la même équipe. Une exception est faite pour les échanges de positions entre deux agents, qui n'est pas permise. (Cela supposerait que les agents se croisent).





### Références
Les références suivantes sont les principales sources d'inspiration pour le projet, n'hésitez pas à les consulter:

1. David Silver. Cooperative Path-Finding. ([article](https://www.davidsilver.uk/wp-content/uploads/2020/03/coop-path-AIWisdom.pdf))
2. Marika Ivanová and Pavel Surynek. Adversarial Cooperative Path-finding: Complexity and Algorithms. ([article](https://surynek.net/publications/files/Ivanova-Surynek_ACPF_ICTAI-2014.pdf))
3. Amit Patel. Red Blob Games. Dealing with moving obstacles ([article](http://theory.stanford.edu/~amitp/GameProgramming/MovingObstacles.html))



## Réalisation demandée

L'objectif de ce projet est de développer et de comparer plusieurs stratégies pour les équipes d'agents.
On considère dans le version de base que chaque agent se voit attribuer un objectif unique, différent pour chaque agent. Il sera possible d'étudier des variantes si vous avez le temps (voir "Pour aller plus loin").  

### Méthodes de résolution envisagées:

Les méthodes suivantes sont données à titre d'exemples, la liste n'est bien sûr pas exhaustive:

* approches heuristiques: déplacements seulement localement optimaux, ie. règles simples basées sur l'état actuel du jeu
* A* indépendants au sein d'une équipe, avec recalcul des chemins en cas de blocage, ou après un certain nombre de pas [3]
* stratégies de réparation locales: path-slicing [3]
* cooperative A* pour une équipe [1]
* alpha-beta, afin de prendre en compte les actions de l'autre équipe et d'essayer d'y répondre au mieux
* Monte-Carlo Tree search
* etc.

Vous devrez pour ce projet:
* coder au moins 3 stratégies différentes pour les équipes;
* mettre en évidence 3 situations intéressantes que vous aurez observées pendant vos tests, en expliquant les choix fait par vos stratégies dans ces situations;
* comparer les résultats de vos stratégies, en mettant en compétition vos équipes sur des cartes denses en obstacles comme `exAdvCoopMap`. On suggère de commencer avec des équipes de 3 à 5 agents par équipe. Vous pourrez répéter les simulations en variant les localisations des agents et des objets dans des zones définies, et donner les moyennes sur les paries simulées, afin d'avoir des résultats significatifs (voir [2]).

On pourra supposer que les informations concernant les positions des agents (équipiers et adversaires) ainsi que des objectifs sont disponibles. Au sein d'une équipe, les agents connaissent aussi l'attribution des objectifs aux autres agents (mais ce n'est pas le cas pour les agents de l'autre équipe). 



## Organisation du template fourni

Le template de code fourni dans ce repertoire est structuré de la manière suivante:
* un répertoire `adv_coop_multiagent_pathfinding`, qui contient les sous-répertoires:
  * `pySpriteWorld` qui contient les modules de gestion des personnages et des cartes. Vous n'avez pas modifier ce code.
Les cartes sont dans un sous-répertoire `Cartes`. Celles-ci sont réalisées avec l'éditeur de cartes [Tiled](https://www.mapeditor.org/), que vous pouvez utiliser pour réaliser vos propres cartes. Elles sont organisées en *layers*: dans notre cas le layer `joueur`, le layer `ramassable` qui contient les objets, et le layer `obstacle` qui contient les murs, arbres, etc.
  * un répertoire `search` qui contient les algos de résolution. Il ne contient pour le moment que A* (repris du code montré en cours et instancié pour les grilles 2D avec la distance de Manhattan).
  * un programme `main.py` qui contient un exemple de code vous permettant de prendre en main l'environnement. Ici, deux joueurs cherchent à aller chercher un objet qui leur est attribué au hasard. Le premier joueur utilise A* pour calculer son chemin, tandis que le deuxième joueur fait une marche aléatoire. Comme vous pouvez l'imaginer, il gagne moins souvent...
  > **Attention**: *aucune gestion des collisions n'est réalisée ici. Les agents peuvent donc parfois se retrouver sur la même case*. Il vous faudra bien sûr gérer ces contraintes dans votre projet. Notez que vous ne devez pas utiliser les fichiers `collision.py` etc. qui empêchent au niveau du jeu les collisions. Ce sont ici les agents qui doivent anticiper ces collisions.

* `docs`, un répertoire vide pour l'instant, qui a vocation a accueillir votre documentation (par exemple vos résultats), et le rapport de fin du projet (qui pourra prendre la forme d'un pdf de 5 pages max, ou d'un notebook).

Le template n'est bien sûr fourni qu'à titre d'exemple, vous pouvez repartir de zéro si vous le souhaitez. Veillez toutefois à conserver la même structure pour le projet.



## Pour aller plus loin
Quelques idées si vous souhaitez aller plus loin :
* permettre d'avoir plus d'agents que d'objectifs, et donc d'avoir des joueurs complètement dédiés à empêcher les joueurs de l'autre équipe d'atteindre leurs objectifs
* permettre à chaque joueur d'avoir un *ensemble d'objectifs*, éventuellement non-disjoints entre les joueurs. Cela pose des questions de changements d'objectif en cours de partie pour certains agents, et nécessite donc une approche particulière. Notez que c'est cette variante qui est étudiée dans la section expérimentale de [2]
