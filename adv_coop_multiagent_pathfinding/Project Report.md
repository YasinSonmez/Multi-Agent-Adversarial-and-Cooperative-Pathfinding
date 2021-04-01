# Implementation

J'ai implémenté 3 algorithmes:
* Local A\* : A* indépendants au sein d'une équipe, avec recalcul des chemins en cas de blocage. 
* Cooperative A\* : Ajouter le temps comme une troisieme dimesion pour eviter collisions.
* Alpha-Beta Minimax : En utilisant la methode de cherche d'arbre, trouver la meilleure strategie evitant les collisions.


# Cooperation

| Algorithm      | Map | Gif|
| :-----------: | :-----------: | :-----------: |
| Local A\*, Cooperative A\*, Alpha-Beta Minimax      |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map2.png" width="250" /> |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/local_map2_coop.gif" width="250" />  |
| Cooperative A\*, Alpha-Beta Minimax   |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map3.png" width="250" />  |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/coop_map3_coop.gif" width="250" />        |
| Alpha-Beta Minimax|<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map4.png" width="250" />  |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/alpha_map4_coop.gif" width="250" />        |

# Adversaires
| Algorithm      | Map | Gif|
| :-----------: | :-----------: | :-----------: |
| Local A\*, Cooperative A\*, Alpha-Beta Minimax      |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/map5.png" width="250" /> |<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/alpha_map5_adv.gif" width="250" />  |


# Local A\* vs Cooperative A\*

* 30 iterations
* Local A\* vs Cooperative A\*
* Buts aleatoires à chaque jeu
* Agents aleatoires à chaque jeu


|Gif | Results|
|:-: | :-: |
|<img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/adversarial.gif" width="400" /> |  <img src="https://github.com/SU-LU3IN025-fev2021/projet-adv-coop-multiagent-pathfinding-yasin-groupe4/blob/main/adv_coop_multiagent_pathfinding/media/local_vs_coop.png" width="500" /> |

