# Redéfinition des fonctions précédemment perdues après l'erreur

# Appariements par plus proche voisin mutuel
def mutual_nn_matches(D):
    matches = []
    for i in range(D.shape[0]):
        j_min = D[i].argmin()
        if D[:, j_min].argmin() == i:
            matches.append((i, j_min))
    return matches

# Vérification des violations de l'inégalité triangulaire
def triangle_violations(D):
    m, n = D.shape
    violations = []
    for i in range(m):  # pour chaque p_i
        for j in range(n):  # candidat t_j
            for k in range(n):  # test de tous les t_k
                if k != j and D[i, k] + levenshtein(T[k], T[j]) < D[i, j]:
                    violations.append((i, j, k))  # p_i à t_j violé via t_k
    return violations

# Score de confiance basé sur la symétrie et les violations
def confidence_scores(D, matches, triangle_violations):
    m_conf = {}
    for i, j in matches:
        is_violated = any(i == vi and j == vj for vi, vj, _ in triangle_violations)
        score = 1.0 if not is_violated else 0.5  # simple scoring
        m_conf[(i, j)] = score
    return m_conf

# Recalcul
matches = mutual_nn_matches(D)
violations = triangle_violations(D)
conf_scores = confidence_scores(D, matches, violations)

# Affichage matrice
plt.figure(figsize=(10, 6))
sns.heatmap(D, annot=True, xticklabels=T, yticklabels=P, cmap="YlGnBu", cbar_kws={'label': 'Levenshtein distance'})
plt.title("Matrice de distances Levenshtein (P vs T)")
plt.xlabel("Vérité terrain")
plt.ylabel("Prédictions")
plt.tight_layout()
plt.show()

(matches, violations, conf_scores)

