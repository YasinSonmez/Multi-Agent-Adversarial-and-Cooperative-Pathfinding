# Implementation

3 algorithmes sont implémentés:
* Local A\*: A * indépendant au sein d'une équipe, avec recalcul des chemins en cas de blocage.
* Coopérative A\*: Ajouter le temps comme troisième dimesion pour éviter les collisions. Les agents peuvent bouger ou attendre pendant certain temps.
* L’élagage Alpha-Beta: En utilisant la méthode de l'arbre de recherche, trouvez la meilleure stratégie pour éviter les collisions.


# Cooperation

| Algorithm      | Map | Gif|
| :-----------: | :-----------: | :-----------: |
| Local A\*, Cooperative A\*, Alpha-Beta      |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map2.png" width="250" /> |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/local_map2_coop.gif" width="250" />  |
| Cooperative A\*, Alpha-Beta   |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map3.png" width="250" />  |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/coop_map3_coop.gif" width="250" />        |
| Alpha-Beta|<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map4.png" width="250" />  |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/alpha_map4_coop.gif" width="250" />        |

# Adversaire
| Algorithm      | Map | Gif|
| :-----------: | :-----------: | :-----------: |
| Alpha-Beta      |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map5.png" width="250" /> |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/alpha_map5_adv.gif" width="250" />  |


# Local A\* vs Cooperative A\*

* 30 itérations
* 50 répétitions de jeu
* Local A\* vs coopérative A\*
* Buts aléatoires dans chaque match
* Agents aléatoires dans chaque jeu

- Coopérative A\* semble avoir un résultat légèrement meilleur que le local A\*. Mais il est beacoup meilleure dans les environments denses.

- Nous ne pouvons pas comparer Alpha-Beta avec les autres algorithmes dans les grandes cartes car il faut trop de temps pour traiter un arbre énorme avec un facteur de branchement énorme.

|Gif | Result|
|:-: | :-: |
|<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/adversarial.gif" width="400" /> |  <img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/local_vs_coop.png" width="500" /> |

|Gif | Result|
|:-: | :-: |
|<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/adversarial_dense.gif" width="400" /> |  <img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/local_vs_coop_dense.png" width="500" /> |

