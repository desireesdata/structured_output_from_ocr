from Levenshtein import distance as levenshtein
from itertools import product

# === Données d'exemple
P = ["semat", "l0i", "1931", "74O"]
T = ["sénat", "loi", "1931", "740", "8"]

# === Étape 1 : calcul de la matrice de distances
D = [[levenshtein(p, t) for t in T] for p in P]

# === Étape 2 : appariements mutuels (symétriques)
mutuals = []
for i, p in enumerate(P):
    j_min = min(range(len(T)), key=lambda j: D[i][j])
    t = T[j_min]
    i_back = min(range(len(P)), key=lambda i_: D[i_][j_min])
    if i_back == i:
        mutuals.append((p, t, i, j_min))

# === Étape 3 : filtrage par cohérence métrique (triangulaire relâchée, version relative)
def filter_brocard_adaptatif(mutuals, D, T, ratio_min=0.8, ratio_max=1.3):
    good = []
    for p, t, i, j in mutuals:
        coherent = False
        for k in range(len(T)):
            if k == j: continue
            d_ij = D[i][j]
            d_ik = D[i][k]
            d_jk = levenshtein(T[j], T[k])
            denom = d_ik + d_jk + 1e-5  # éviter division par zéro
            ratio = d_ij / denom
            if ratio_min <= ratio <= ratio_max:
                coherent = True
                break
        if coherent:
            good.append((p, t))
    return good

# === Application du filtre
final_matches = filter_brocard_adaptatif(mutuals, D, T)

# === Affichage final
print("✅ Appariements mutuels et cohérents (Brocard-relâché adaptatif) :")
for p, t in final_matches:
    print(f"  {p} ⟷ {t}")
