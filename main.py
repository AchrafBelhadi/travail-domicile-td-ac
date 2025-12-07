"""

 TD3 – Algorithmique & Complexité
 Exercice 4 + Exercice 5
===========================================================

Ce fichier contient :
- Une heuristique pour résoudre le TSP (Exercice 4)
- Une petite démonstration de pourquoi le TSP est NP-difficile (Exercice 5)
- Les explications théoriques écrites simplement dans les commentaires
"""

# ---------------------------------------------------------
#  EXERCICE 4 – Méthode heuristique (Recuit simulé)
# ---------------------------------------------------------
"""
Pourquoi une heuristique ?
-------------------------
Le TSP exact devient rapidement impossible à résoudre quand le nombre de villes augmente,
car le nombre de permutations explose (n! → énorme). Pour 10 villes ça passe, mais pour
58 wilayas c’est absolument impossible en brute-force.

Le recuit simulé (Simulated Annealing) :
----------------------------------------
L’idée est simple : on commence avec une tournée (souvent aléatoire), puis on essaye
de l’améliorer progressivement. On autorise parfois des solutions plus mauvaises au début
pour éviter de rester coincé dans un minimum local. Plus la “température” baisse,
moins on accepte de mauvais changements.

Complexité : en gros O(nb_iterations × n), très raisonnable pour n=10.
"""

import math
import random

# Les 10 wilayas et la matrice de distances donnée dans l’énoncé
wilayas = [
    "Alger","Batna","Oran","Sétif","Constantine",
    "Tlemcen","Ouargla","Annaba","Béchar","Tizi-Ouzou"
]

D = [
    [0,430,415,260,320,520,770,600,970,110],
    [430,0,798,100,120,620,420,300,950,350],
    [415,798,0,430,500,180,850,780,720,380],
    [260,100,430,0,115,500,620,310,800,250],
    [320,120,500,115,0,550,610,160,950,340],
    [520,620,180,500,550,0,1000,720,450,540],
    [770,420,850,620,610,1000,0,720,770,640],
    [600,300,780,310,160,720,720,0,1150,360],
    [970,950,720,800,950,450,770,1150,0,1160],
    [110,350,380,250,340,540,640,360,1160,0]
]

# -----------------------------------------------------
# Fonctions utilitaires
# -----------------------------------------------------

def cost(tour):
    """Calcule le coût total d’une tournée (cycle)."""
    total = 0
    for i in range(len(tour) - 1):
        total += D[tour[i]][tour[i+1]]
    total += D[tour[-1]][tour[0]]  # retour à la ville de départ
    return total

def random_neighbor(tour):
    """Génère un voisin en échangeant deux villes au hasard."""
    a, b = random.sample(range(len(tour)), 2)
    new = tour[:]
    new[a], new[b] = new[b], new[a]
    return new

# -----------------------------------------------------
#  Recuit simulé
# -----------------------------------------------------

def simulated_annealing(iterations=8000, T0=1500, alpha=0.997):
    n = len(wilayas)
    current = list(range(n))
    random.shuffle(current)

    current_cost = cost(current)
    best = current[:]
    best_cost = current_cost

    T = T0

    for _ in range(iterations):
        neighbor = random_neighbor(current)
        neighbor_cost = cost(neighbor)
        delta = neighbor_cost - current_cost

        # Accepter toujours si meilleur
        # ou parfois si la solution est pire
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            current_cost = neighbor_cost

        # Mettre à jour le meilleur trouvé
        if current_cost < best_cost:
            best = current[:]
            best_cost = current_cost

        T *= alpha  # refroidissement

    return best, best_cost


# ---------------------------------------------------------
#  EXERCICE 5 – NP-difficile : réduction HC -> TSP
# ---------------------------------------------------------
"""
Explication simple :
--------------------
Pour montrer que le TSP est NP-difficile, on réduit un problème
déjà connu comme NP-Complet : le cycle hamiltonien (Hamiltonian Cycle).

Idée de la réduction :
- Si une arête existe dans le graphe → distance = 1
- Sinon → distance = 2
- Et on met K = n (le nombre de sommets)

Ainsi :
- S’il existe un cycle hamiltonien, il coûtera exactement n
- Sinon, toute tournée coûte au moins n+1

Donc le TSP-décision est NP-Complet → et la version optimisation est NP-difficile.

Définitions rapides :
---------------------
P : problème résolu en temps polynomial
NP : on peut vérifier une solution en polynomial
NP-Complet : dans NP + aussi difficile que tous les problèmes de NP
NP-Difficile : au moins aussi difficile que les NP-Complet, pas forcément dans NP
"""

def reduce_HC_to_TSP(adj):
    """Transforme une matrice d’adjacence HC en matrice TSP réduite."""
    n = len(adj)
    tsp = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                tsp[i][j] = 0
            elif adj[i][j] == 1:   # arête existe
                tsp[i][j] = 1
            else:                 # arête absente
                tsp[i][j] = 2

    return tsp


# Petit exemple : graphe simple contenant un cycle 0-1-2-3-0
HC_example = [
    [0,1,0,1],
    [1,0,1,0],
    [0,1,0,1],
    [1,0,1,0]
]

tsp_example = reduce_HC_to_TSP(HC_example)

# ---------------------------------------------------------
#   Lancer les deux exercices
# ---------------------------------------------------------


print(" Résultats – Exercice 4 (Recuit simulé)")


best_tour, best_length = simulated_annealing()
print("Meilleure tournée (index) :", best_tour)
print("Tournée (wilayas) :", [wilayas[i] for i in best_tour])
print("Longueur totale :", best_length)



print(" Résultats – Exercice 5 (Réduction HC → TSP)")


print("Matrice HC :")
for row in HC_example:
    print(row)

print("\nMatrice TSP obtenue :")
for row in tsp_example:
    print(row)

print("\nSeuil K =", len(HC_example))
print("→ Démonstration que le TSP est NP-difficile.\n")
